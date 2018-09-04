import re
import time

from server import log
from server.database import db
from server.models.long_term_vehicle import LongTermVehiclModel
from server.models.message import MessageSystemModel


def background_thread():
    """后台监控程序，10分钟监控数据库一次，检查数据库变化，如果有变化，将对应信息写到信息表"""
    new_count = 0
    last_count = 0
    count = 1
    while True:
        log.info('第%d次后台监控定时任务开始,当前时间是%s' % (count, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        now_count = LongTermVehiclModel.get_count(db.read_db)
        print('当前长期用车消息的数量:', now_count)
        if now_count and last_count:
            new_count = now_count - last_count
        if new_count and new_count > 0:
            print('有新的长期用车消息,数量为:', new_count)
            new_data = LongTermVehiclModel.get_data(db.read_db, new_count)
            if new_data:
                try:
                    # 处理长期用车数据
                    new_data = handle(new_data)
                    # 将新添加的长期用车信息写进系统信息表
                    for detail in new_data:
                        region_id = detail.get('region_id')
                        msg_id = MessageSystemModel.insert_system_message(db.write_bi, detail)
                        data = []
                        # 将数据发送给对应地区的城市经理
                        city_manager_list = MessageSystemModel.get_city_manager_by_region_id(db.read_bi, region_id)
                        for city_manager in city_manager_list:
                            data.append({
                                'account': city_manager['account'],
                                'role': city_manager['role'],
                                'sys_msg_id': msg_id,
                                'create_time': int(time.time()),
                                'update_time': int(time.time())
                            })
                            MessageSystemModel.insert_user_message(db.write_bi, data)
                        data.clear()
                        # 将数据发送给对应地区的区镇合伙人和网点管理人
                        # 区镇合伙人
                        suppliers_user_list = MessageSystemModel.get_suppliers_user_by_region_id(db.read_db, region_id)
                        # 网点管理员
                        supplier_nodes_user_list = MessageSystemModel.get_supplier_nodes_by_region_id(db.read_db,
                                                                                                      region_id)
                        suppliers_user_account_list = [i.get('account') for i in suppliers_user_list]
                        for i in supplier_nodes_user_list:
                            if i.get('account') not in suppliers_user_account_list:
                                suppliers_user_list.append(i)

                        for supplier in suppliers_user_list:
                            data.append({
                                'account': supplier['account'],
                                'role': supplier['role'],
                                'sys_msg_id': msg_id,
                                'create_time': int(time.time()),
                                'update_time': int(time.time())
                            })
                        MessageSystemModel.insert_user_message(db.write_bi, data)
                        data.clear()
                        log.info('消息推送成功,消息id是:{}'.format(msg_id))
                except Exception as e:
                    log.error('消息推送失败,错误原因是:{}'.format(e))
        last_count = now_count
        print('上一次长期用车消息的数量:', last_count)
        # 下次更新推送消息时隔10分钟
        log.info('第%d次后台监控定时任务完成,当前时间是%s' % (count, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        count += 1
        print('\n')
        time.sleep(10)


def handle(data):
    title = '长期用车'
    user_id = 322
    msg_type = 2
    for detail in data:
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
            data = []
    return data

