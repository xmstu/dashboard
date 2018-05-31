import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.status import HTTPStatus, make_result, APIStatus


class User(object):

    def get(self):
        pass


class UserList(object):

    @staticmethod
    @make_decorator
    def check_params(page, limit, params):

        try:
            # 通过params获取请求的参数，不管参数有没有值，都会给一个默认值，避免多次检验

            user_name = params.get('user_name') if params.get('user_name') else ''
            mobile = params.get('mobile') if params.get('mobile') else ''
            reference_mobile = params.get('reference_mobile') if params.get('reference_mobile') else ''
            download_channel = params.get('download_channel') if params.get('download_channel') else ''
            from_channel = params.get('from_channel') if params.get('from_channel') else ''

            is_referenced = int(params.get('is_referenced')) if params.get('is_referenced') else 0

            provinceid = int(params.get('provinceid')) if params.get('provinceid') else 0
            regionid = int(params.get('regionid')) if params.get('regionid') else 0
            cityid = int(params.get('cityid')) if params.get('cityid') else 0
            townid = int(params.get('townid')) if params.get('townid') else 0

            role_type = int(params.get('role_type')) if params.get('role_type') else 0
            role_auth = int(params.get('role_auth')) if params.get('role_auth') else 0
            is_actived = int(params.get('is_actived')) if params.get('is_actived') else 0
            is_used = int(params.get('is_used')) if params.get('is_used') else 0
            is_car_sticker = int(params.get('is_car_sticker')) if params.get('is_car_sticker') else 0

            last_login_start_time = int(params.get('last_login_start_time')) if params.get(
                'last_login_start_time') else 0
            last_login_end_time = int(params.get('last_login_end_time')) if params.get('last_login_end_time') else 0

            register_start_time = int(params.get('register_start_time')) if params.get('register_start_time') else 0
            register_end_time = int(params.get('register_end_time')) if params.get('register_end_time') else 0

            # 检验最后登陆时间
            if not (last_login_start_time and last_login_end_time):
                pass
            elif last_login_start_time and last_login_end_time:
                if (last_login_end_time > last_login_start_time) and (last_login_end_time < time.time()):
                    pass
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='最后登录时间有误'))

            # 检验注册时间
            if not (register_start_time and register_end_time):
                pass
            elif register_start_time and register_end_time:
                if (register_end_time > register_start_time) and (register_end_time < time.time()):
                    pass
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='选择的注册时间有误'))

            params = {'user_name': user_name,
                      'mobile': mobile,
                      'reference_mobile': reference_mobile,
                      'download_channel': download_channel,
                      'from_channel': from_channel,
                      'is_referenced': is_referenced,
                      'provinceid': provinceid,
                      'cityid': cityid,
                      'townid': townid,
                      'regionid': regionid,
                      'role_type': role_type,
                      'role_auth': role_auth,
                      'is_actived': is_actived,
                      'is_used': is_used,
                      'is_car_sticker': is_car_sticker,
                      'last_login_start_time': last_login_start_time,
                      'last_login_end_time': last_login_end_time,
                      'register_start_time': register_start_time,
                      'register_end_time': register_end_time}

        except Exception as e:
            log.info("Error:{}".format(e))

        log.info("Response:{}".format(params))

        return Response(page=page, limit=limit, params=params)
