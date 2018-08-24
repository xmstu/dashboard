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
    count = 0
    while True:
        now_count = LongTermVehiclModel.get_count(db.read_db)
        print(now_count)
        if now_count and last_count:
            new_count = now_count - last_count
        if new_count:
            new_data = LongTermVehiclModel.get_data(db.read_db, new_count)
            if new_data:
                try:
                    # 处理长期用车数据
                    new_data = handle(new_data)
                    # 将新添加的长期用车信息写进系统信息表
                    for detail in new_data:
                        msg_id = MessageSystemModel.insert_system_message(db.write_bi, detail)
                        # 将数据发送给对应地区的城市经理或区镇合伙人
                        data = []
                        user_list = MessageSystemModel.get_system_user(db.read_db)
                        for user in user_list:
                            data.append({
                                'account': user['account'],
                                'role': user['role'],
                                'sys_msg_id': msg_id,
                                'create_time': int(time.time()),
                                'update_time': int(time.time())
                            })
                            MessageSystemModel.insert_user_message(db.write_bi, data)
                except Exception as e:
                    log.error('消息推送失败,错误原因是:{}'.format(e))
        last_count = now_count
        print(last_count)
        # 下次更新推送消息时隔10分钟
        count += 1
        print('第%d次后台监控定时任务完成' % count)
        time.sleep(10)


def handle(data):
    title = '长期用车'
    user_id = 322
    msg_type = 2
    for detail in data:
        detail.setdefault('title', title)
        detail.setdefault('user_id', user_id)
        detail.setdefault('msg_type', msg_type)

        # content = detail.get('content', '')
        # load_address = re.search('装货-地址：(.*?)<br>', content).group(1)
        # print(load_address)
        #
        # unload_address = re.search('卸货-地址：(.*?)<br>', content).group(1)
        # print(unload_address)
        #
        # long_lat = re.findall('(\d+\.\d+)', content)
        # print(long_lat)

    return data
