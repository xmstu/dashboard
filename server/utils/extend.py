from functools import wraps
import hashlib
import random
import re
import time

import logging
import pymongo
import redis
import requests

from server import configs, modules, log
from server.workflow.utils import performance


def parameter_sign(secret, parameters):
    # ===========================================================================
    # '''签名方法
    # @param secret: 签名需要的密钥
    # @param parameters: 支持字典和string两种
    # '''
    # ===========================================================================
    # 如果parameters 是字典类的话
    if hasattr(parameters, "items"):
        keys = list(parameters.keys())
        keys.sort()

        parameters = "%s%s%s" % (secret,
                                 str().join('%s%s' % (key, parameters[key]) for key in keys),
                                 secret)

    m = hashlib.md5()
    m.update(parameters.encode())
    sign = m.hexdigest().upper()
    return sign


class ExtendRedis(object):
    logger = log

    def __init__(self, ip='127.0.0.1', port='6379', db=0, name='token'):

        self.ip = configs.remote.union.redis[name].host
        self.port = configs.remote.union.redis[name].port
        self.db = configs.remote.union.redis[name].db
        try:
            self.conn = redis.StrictRedis(host=self.ip, port=self.port, db=self.db)
        except Exception as err:
            self.conn = object()

    def write_one(self, key, value):
        try:
            if not isinstance(value, dict):
                return False
            data = self.conn.set(key, value)
            return data
        except Exception as err:
            self.logger.error('错误%s:' % err)
            return False

    def write_ex(self, key, value, timeout=0):
        try:
            data = self.conn.setex(key, timeout, value)
            return data
        except Exception as err:
            self.logger.error('错误%s:' % err)
            return False

    def read_one(self, key):
        try:
            data = self.conn.get(key)
            if not data:
                return
            data = eval(data.decode('utf8'))
            return data
        except Exception as err:
            self.logger.error('错误%s:' % err)
            return False

    def delete(self, key):
        try:
            data = self.conn.get(key)
            if not data:
                return True
            result = self.conn.delete(key)
            if not result:
                return False
            return True
        except Exception as err:
            self.logger.error('错误%s:' % err)
            return False

    def check_token(self, token):
        try:
            result = self.conn.hget('user.online:' + token, 'token')
            if not result:
                return False
            user_id = self.conn.hget('user.online:' + token, 'user_id')
            if not user_id:
                return False
            return user_id
        except Exception as err:
            self.logger.error('错误%s:' % err)
            return False

    def update_token(self, token, user_id, expire_time=7200):
        """更新用户的TOKEN
        :param token: 用户获取的TOKEN
        :param user_id:  用户ID
        :param expire_time: 有效时间
        """
        try:
            if not token:
                return False
            loading_time = int(time.time())
            self.conn.hset('user.online:' + token, 'token', token)
            self.conn.hset('user.online:' + token, 'user_id', user_id)
            self.conn.hset('user.online:' + token, 'login_time', loading_time)
            self.conn.expire('user.online:' + token, expire_time)
        except Exception as err:
            self.logger.error('错误%s:' % err)
            return False

    def clear_token(self, token):
        "清除用户登录的TOKEN"
        try:
            self.conn.delete('user.online:' + token)
            self.logger.info('clear_token %s' % token)
            # self.conn.hdel('user.online:' + token, 'token')
            # self.conn.hdel('user.online:' + token, 'user_id')
            # self.conn.hdel('user.online:' + token, 'login_time')
        except Exception as err:
            self.logger.error('错误%s:' % err)
            return False


class MongLinks(object):
    def __init__(self, target='locations', distriction="user_locations"):
        ip = configs.remote.union.mongo[target].host
        port = configs.remote.union.mongo[target].port
        db = configs.remote.union.mongo[target].db
        try:
            user = configs.remote.union.mongo[target].user
            password = configs.remote.union.mongo[target].password
        except:
            user = None
            password = None
        self.conn = pymongo.MongoClient(host=ip, port=port)
        if user and password:
            db_auth = self.conn[db]
            db_auth.authenticate(user, password)
            self.remote_db = self.conn[db][distriction]
        else:
            self.remote_db = self.conn[db][distriction]

        self.db = db


class Check(object):
    @staticmethod
    def is_mobile(mobile) -> bool:
        if mobile and str(mobile).isdigit():
            return bool(re.findall('1[23456789]{1}['
                                   '0-9]{9}', str(mobile)))
        return False

    @staticmethod
    def is_pwd(pwd) -> bool:
        return bool(re.findall('^[a-zA-Z0-9]\w{5,15}$', str(pwd)))

    @staticmethod
    def is_code(code) -> bool:
        return code and str(code).isdigit()

    @staticmethod
    def is_captcha_type(_type) -> bool:
        return _type and str(_type).isdigit() and int(_type) in (1, 2, 3, 4, 5, 6)

    @staticmethod
    def is_platform(platform) -> bool:
        return platform and str(platform).isdigit() and int(platform) in (1, 2, 3, 4, 5, 6)

    @staticmethod
    def is_user_type(_type) -> bool:
        return _type and str(_type).isdigit() and int(_type) in (1, 2, 3)


class Limit(object):
    # 检测是否频繁请求，redis中存有loging_15917907641: 5，key为loging_15917907641，5为请求次数

    @staticmethod
    def ok(key: str, timeout=600) -> bool:
        try:
            _redis = ExtendRedis(name='token')
            count = _redis.conn.get(key)
            log.info('count:{}'.format(count))
            if not count:
                _redis.write_ex(key, 1, timeout=timeout)
            else:
                if int(count) > 10:
                    return False
                _redis.write_ex(key, int(count) + 1, timeout=timeout)
        except Exception as err:
            log.error('错误%s:\n%s' % (key, err), exc_info=True)
        finally:
            return True


class ExtendHandler(object):
    """扩展类

    """

    @staticmethod
    def handler(obj):
        """转换函数

        :param obj: 传递的函数
        :return   : String
        """
        return obj.isoformat() if hasattr(obj, 'isoformat') else str(obj)

    @staticmethod
    def image_replace(url):
        """
        :param url: 连接字符串
        :return   : 字典
        """
        url = url if url else ''
        if not url:
            return {'s': '', 'l': ''}
        return {'s': url + '?32*32', 'l': url + '?64*64'}

    @staticmethod
    def fetch_area():
        """获取地区并存入字典返回

        """
        area_sql = "SELECT `code`, `name` FROM `shm_regions`"
        area_data = modules.read_io.query(area_sql)
        area = dict([(x['code'], x['name']) for x in area_data])
        if not area:
            return {}
        return area

    @staticmethod
    def format_addr(province, city, county, area={}, lat=0, lon=0, addr=''):
        """
        localtion JSON格式
        """
        if not area:
            area = ExtendHandler.fetch_area()

        location = {"province": {'id': province, 'name': area.get(str(province), '未知')},
                    "city": {'id': city, 'name': area.get(str(city), '未知')},
                    "county": {'id': county, 'name': area.get(str(county), '未知')}
                    }
        if addr:
            location.update({'address': addr})
        if lat and lon:
            location.update({'latitude': lat, 'longitude': lon})
        return location

    @staticmethod
    @performance(log=log, level=logging.INFO)
    def send_code(mobile, code, op="用户注册"):
        """ 发送验证码
        :param mobile: 电话号码
        :param code  : 验证码
        :param op    : 类型  
        :return      : 请求状态
        :rtype       : dict
        """
        # apiUrl='http://p.msg.huitouche.com/sms/dayu/code?secret=Jkdieo2j0sDE954654KLD'
        # payload = {}
        # payload['mobile']=mobile
        # payload['code']=code
        # payload['operation']=op
        # result = ExtendHandler.push_content('-1', push_type="captcha_register", params=payload, async=True)
        apiUrl = configs.remote.union.msg.url + 'sms/'
        # apiUrl = 'http://192.168.10.125:5000/' + 'sms/'
        payload = {
            "mobiles": "%s" % mobile,
            "template_id": "JSMS_137903",
            "template_args": '{"code": "%s", "operation": "%s"}' % (code, op)
        }
        app_key = configs.remote.union.msg.app_key
        app_secret = configs.remote.union.msg.app_secret
        timestamp = int(time.time())
        payload.update({'timestamp': timestamp})
        sign_str = parameter_sign(app_secret, payload)
        del payload['timestamp']
        r = requests.post(apiUrl + '?app_key=%s&sign=%s&timestamp=%s' % (app_key, sign_str, timestamp), json=payload)
        if r.status_code == 200:
            result = r.json()
            result.update({'state': 1})
            log.info('SendCodeResult:{}'.format(result))
            return result
        else:
            modules.log.error("请求状态：%d, 内容%s" % (r.status_code, r.text))
            return {'state': 0}

    @staticmethod
    @performance(log=log, level=logging.INFO)
    def register_msg_plus(mobile, user_id):
        """ 注册通讯用户

        :params mobile  : 电话
        :params password: 密码
        :params user_id : 用户ID

        """
        # apiUrl = "http://192.168.10.125:5000/im/users/"
        apiUrl = configs.remote.union.msg.url + 'im/users/'
        app_key = configs.remote.union.msg.app_key
        app_secret = configs.remote.union.msg.app_secret
        timestamp = int(time.time())
        pwd = "".join([random.choice([i for i in "wertyjukicvbnmrty4567u8i213"]) for k in range(10)])
        pwd = hashlib.md5(pwd.encode("utf8"))
        pwd = pwd.hexdigest()

        if configs.env.deploy == "dev":
            username = 'd' + str(user_id).zfill(4)
        elif configs.env.deploy == "uat":
            username = 'u' + str(user_id).zfill(4)
        else:
            username = 'p' + str(user_id).zfill(4)

        payload = {
            "password": pwd,
            "username": username,
            "nickname": "消息"
        }

        # modules.log.info(payload)
        payload.update({'timestamp': timestamp})
        sign_str = parameter_sign(app_secret, payload)

        del payload['timestamp']
        r = requests.post(apiUrl + '?app_key=%s&sign=%s&timestamp=%s' % (app_key, sign_str, timestamp), json=payload)

        # modules.log.info(r.text);
        if r.status_code == 200:
            return payload
        return False

    @staticmethod
    def send_msg(mobile, content):
        apiUrlXh = 'http://p.msg.huitouche.com/sms/xiehe?secret=Jkdieo2j0sDE954654KLD'
        payload = {'mobile': mobile, 'msg': content}
        r = requests.post(apiUrlXh, data=payload)
        result = r.json()
        if not result:
            return {'state': 0}
        return result

    @staticmethod
    def write_password(pwd):
        m = hashlib.md5(pwd.encode('utf8'))
        return m.hexdigest()

    @staticmethod
    def escaps_fromat(**kwarg):
        pass

    @staticmethod
    @performance(log=log, level=logging.INFO)
    def push_content(user_id, push_type='force_logout', params={}):
        """ 推送方法
        :param user_id  : 推送的用户
        :param push_type: 推送的类型
        :param content  : 推送的内容
        :return Bool    : 返回成功和失败
        """
        push_msg = {
            "user_ids": "%s" % user_id,
            "params": params,
            "to_all_user": 0,
            "code": push_type
        }
        try:
            api_url = configs.remote.union.messager.url
            r = requests.post(api_url, json=push_msg)
            print(api_url, push_msg)
            if r.status_code == 200:
                return True
            else:
                modules.log.debug('消息没有推送成功 push_msg: %s' % push_msg)
        except Exception as e:
            modules.log.debug('消息服务器连接错误 %s %s' % (push_msg, e), exc_info=True)
        return False

    @staticmethod
    @performance(log=log, level=logging.INFO)
    def send_push_logout(device_id, client_platform):
        """
        强制下线
        """
        apiUrl = configs.remote.union.msg.url + 'push/'
        if client_platform == 1:
            client_platform = 'android'
        elif client_platform == 2:
            client_platform = 'ios'
        else:
            return False

        payload = {
            'title': '您的账号正在其他设备进行登录，您已被迫下线',
            'extras': '{"route": "{\\"force_jump\\": true, \\"page\\": \\"sshtc://login/\\", \\"force_login\\": true, \\"type\\": \\"local\\"}"}',
            'content': '您的账号正在其他设备进行登录，您已被迫下线',
            'device_ids': device_id,
            'client_platform': client_platform,
            'android_uri_activity': 'com.huitouche.android.app.ui.user.setting.PwdLoginActivity',
            'silent': 0,
            'sound': ''
        }
        app_key = configs.remote.union.msg.app_key
        app_secret = configs.remote.union.msg.app_secret
        timestamp = int(time.time())
        payload.update({'timestamp': timestamp})
        sign_str = parameter_sign(app_secret, payload)
        del payload['timestamp']
        r = requests.post(apiUrl + '?app_key=%s&sign=%s&timestamp=%s' % (app_key, sign_str, timestamp), json=payload)
        if r.status_code == 200:
            result = r.json()
            result.update({'state': 1})
            return result
        else:
            modules.log.error("请求状态：%d, 内容%s" % (r.status_code, r.text))
            return {'state': 0}

    @staticmethod
    def fetch_region_one(region_id):
        region_redis = ExtendRedis(name='region')
        name = region_redis.conn.hget('online.region' + str(region_id), 'name')
        if not name:
            desc = modules.read_io.query_one('SELECT `name` FROM shm_regions WHERE id = %s' % region_id)
            return {'id': region_id, 'name': desc.get('name', '') if desc else ''}
        return {'id': region_id, 'name': name or ''}


def fn_performance(fn):
    def wrapper(function):
        @wraps(function)
        def function_timer(*args, **kwargs):
            t0 = time.time()

            result = function(*args, **kwargs)

            t1 = time.time()

            fn(function, t1 - t0)
            return result

        return function_timer

    return wrapper

