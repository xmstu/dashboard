from server.meta.decorators import make_decorator
from server.status import build_result, build_result_1, APIStatus, HTTPStatus
import time

class MessageSystem(object):
    @staticmethod
    @make_decorator
    def get_result(count, data):
        # 时间格式化
        for i in data:
            i['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i['create_time']))
            i['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i['update_time']))
        return build_result(APIStatus.Ok, data=data, count=count), HTTPStatus.Ok

class MessageUser(object):
    @staticmethod
    @make_decorator
    def get_result(count, unread, data):
        is_read = []
        un_read = []
        # 时间格式化
        for i in data:
            i['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i['create_time']))
            if i['is_read'] == 0:
                un_read.append(i)
            else:
                is_read.append(i)
        # 排序
        un_read.sort(key=lambda x: x['create_time'], reverse=True)
        is_read.sort(key=lambda x: x['create_time'], reverse=True)

        return build_result_1(APIStatus.Ok, data=un_read+is_read, count=count, unread=unread), HTTPStatus.Ok