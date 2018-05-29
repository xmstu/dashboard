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
    def check_paging(pages, limit, **kwargs):
        # 检验pages, limit是否为整数
        if not str(pages).isdigit() or int(pages) <= 0:
            abort(HTTPStatus.BadRequest, **make_result(HTTPStatus.BadRequest, msg='pages参数不能为%s' % pages))

        if not str(limit).isdigit() or (int(limit) not in [10, 20, 30, 40, 50, 300]):
            abort(HTTPStatus.BadRequest, **make_result(HTTPStatus.BadRequest, msg='count参数不能为%s' % limit))

        log.info("params:{}".format(kwargs))
        return Response(pages=pages, limit=limit, **kwargs)

    @staticmethod
    @make_decorator
    def check_params(pages, limit, params):

        # 通过params获取请求的参数，不管参数有没有值，都会给一个默认值，避免多次检验

        user_name = params.get('user_name', '')
        mobile = params.get('mobile', '')
        reference_mobile = params.get('reference_mobile', '')
        download_channel = params.get('download_channel', '')
        from_channel = params.get('from_channel', '')
        is_referenced = int(params.get('is_referenced', 0))
        home_station_id = int(params.get('home_station_id', 0))
        role_type = int(params.get('role_type', 0))
        role_auth = int(params.get('role_auth', 0))
        is_actived = int(params.get('is_actived', 0))
        is_used = int(params.get('is_used', 0))
        is_car_sticker = int(params.get('is_car_sticker', 0))

        last_login_start_time = int(params.get('last_login_start_time', 0))
        last_login_end_time = int(params.get('last_login_end_time', 0))

        register_start_time = int(params.get('register_start_time', 0))
        register_end_time = int(params.get('register_end_time', 0))

        # 检验最后登陆时间
        if not (last_login_start_time and last_login_end_time):
            pass
        elif last_login_start_time and last_login_end_time:
            if (last_login_end_time > last_login_start_time) and (last_login_end_time > time.time()):
                pass
        else:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='最后登录时间有误'))

        # 检验注册时间
        if not (register_start_time and register_end_time):
            pass
        elif register_start_time and register_end_time:
            if (register_end_time > register_start_time) and (register_end_time > time.time()):
                pass
        else:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='选择的注册时间有误'))

        params = {'user_name': user_name, 'mobile': mobile, 'reference_mobile': reference_mobile,
                  'download_channel': download_channel,
                  'from_channel': from_channel, 'is_referenced': is_referenced, 'home_station_id': home_station_id,
                  'role_type':role_type, 'role_auth': role_auth,
                  'is_actived': is_actived, 'is_used': is_used, 'is_car_sticker': is_car_sticker,
                  'last_login_start_time': last_login_start_time, 'last_login_end_time': last_login_end_time,
                  'register_start_time': register_start_time, 'register_end_time': register_end_time}

        log.info("Response:{}".format(params))

        return Response(pages=pages, limit=limit, params=params)
