import time

from flask_restful import abort

from server.meta.decorators import make_decorator, Response
from server.status import HTTPStatus, make_result, APIStatus


class PromoteEffect(object):

    @staticmethod
    @make_decorator
    def check_params(page, limit, params):

        # 通过params获取参数，获取不到就赋予默认值
        user_name = params.get('user_name', '')
        mobile = params.get('mobile', '')
        region_id = int(params.get('region_id', 0))
        role_type = int(params.get('role_type', 0))
        goods_type = int(params.get('goods_type', 0))
        is_actived = int(params.get('is_actived', 0))
        is_car_sticker = int(params.get('is_car_sticker', 0))
        start_time = params.get('start_time', '')
        end_time = params.get('end_time', '')

        # 判断时间是否合法
        if not (start_time and end_time):
            pass
        elif start_time and end_time:
            # 如果时间存在，则强转一下类型
            start_time = int(start_time)
            end_time = int(end_time)
            if (end_time > start_time) and (end_time < time.time()):
                pass
        else:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间有误'))

        # 构造请求参数
        params = {'user_name': user_name, 'mobile': mobile, 'region_id': region_id, 'role_type': role_type,
                  'goods_type': goods_type, 'is_actived': is_actived, 'is_car_sticker': is_car_sticker,
                  'start_time': start_time, 'end_time': end_time}

        return Response(page, limit, params)
