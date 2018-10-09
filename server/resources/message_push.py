import re
import time

from server import log, configs
from server.database import db
from server.failover.electioneer import ElectioneerKazooEngine, Electioneer
from server.models.long_term_vehicle import LongTermVehiclModel
from server.models.message import MessageSystemModel


class BackgroundThread:

    def __init__(self):
        self._read_db = db.read_db
        self._write_db = db.write_db
        self._read_bi = db.read_bi
        self._write_bi = db.write_bi
        self._new_count = 0
        self._last_count = 0
        self._now_count = 0
        self._run_count = 1
        self._data = []

    def get_now_count(self):
        now_count = LongTermVehiclModel.get_count(self._read_db)
        return now_count

    def get_new_data(self):
        new_data = LongTermVehiclModel.get_data(self._read_db, self._new_count)
        return new_data

    def insert_sys_msg(self, detail):
        return MessageSystemModel.insert_system_message(self._write_bi, detail)

    def send_msg_to_city_manager(self, region_id, msg_id):
        city_manager_list = MessageSystemModel.get_city_manager_by_region_id(self._read_bi, region_id)
        for city_manager in city_manager_list:
            self._data.append({
                'account': city_manager['account'],
                'role': city_manager['role'],
                'sys_msg_id': msg_id,
                'create_time': int(time.time()),
                'update_time': int(time.time())
            })
            if self._data:
                MessageSystemModel.insert_user_message(self._write_bi, self._data)
        self._data.clear()

    def send_msg_to_suppliers(self, region_id, msg_id):
        suppliers_user_list = MessageSystemModel.get_suppliers_user_by_region_id(self._read_db, region_id)
        supplier_nodes_user_list = MessageSystemModel.get_supplier_nodes_by_region_id(self._read_db, region_id)
        suppliers_user_account_list = [i.get('account') for i in suppliers_user_list]
        for i in supplier_nodes_user_list:
            if i.get('account') not in suppliers_user_account_list:
                suppliers_user_list.append(i)

        for supplier in suppliers_user_list:
            self._data.append({
                'account': supplier['account'],
                'role': supplier['role'],
                'sys_msg_id': msg_id,
                'create_time': int(time.time()),
                'update_time': int(time.time())
            })
        if self._data:
            MessageSystemModel.insert_user_message(db.write_bi, self._data)
        self._data.clear()

    def auto_send_msg(self, new_data):
        try:
            new_data = self.handle(new_data)
            for detail in new_data:
                region_id = detail.get('region_id')
                msg_id = self.insert_sys_msg(detail)
                self.send_msg_to_city_manager(region_id, msg_id)
                self.send_msg_to_suppliers(region_id, msg_id)
                log.info('消息推送成功,消息id是:{}'.format(msg_id))
        except Exception as e:
            log.error('消息推送失败,错误原因是:{}'.format(e))

    def start(self):
        """后台监控程序，10分钟监控数据库一次，检查数据库变化，如果有变化，将对应信息写到信息表"""
        while True:
            self.background_task()
            time.sleep(10)

    def background_task(self):
        log.info('第%d次后台监控定时任务开始,当前时间是%s' % (self._run_count, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        self._now_count = self.get_now_count()
        print('当前长期用车消息的数量:', self._now_count)
        if self._now_count and self._last_count:
            self._new_count = self._now_count - self._last_count
        if self._new_count and self._new_count > 0:
            print('有新的长期用车消息,数量为:', self._new_count)
            new_data = self.get_new_data()
            if new_data:
                self.auto_send_msg(new_data)

        self._last_count = self._now_count
        print('上一次长期用车消息的数量:', self._last_count)
        # 下次更新推送消息时隔10分钟
        log.info('第%d次后台监控定时任务完成,当前时间是%s' % (self._run_count, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        self._run_count += 1
        print('\n')

    @staticmethod
    def handle(new_data):
        title = '长期用车'
        user_id = 1
        msg_type = 2
        for detail in new_data:
            detail.setdefault('title', title)
            detail.setdefault('user_id', user_id)
            detail.setdefault('msg_type', msg_type)

            content = detail.get('content', '')
            try:
                ret = re.search('装货-省id：(\d{0,6})， 市id：(\d{0,6})， 区id：(\d{0,6})， 镇id：(\d{0,9})', content)
                region_id = ','.join([ret.group(1), ret.group(2), ret.group(3), ret.group(4)])
                detail.setdefault('region_id', region_id)
            except Exception as e:
                log.error('长期用车信息匹配错误，错误原因是:{}'.format(e))
                new_data = []
        return new_data


background_thread = BackgroundThread()

_engine = ElectioneerKazooEngine(hosts=configs.env.zookeeper.host)
election = Electioneer(engine=_engine, path=configs.remote.da_msg_push, identifier=None, election_func=background_thread.start)
