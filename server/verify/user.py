from server.meta.decorators import make_decorator, Response


class User(object):

    def get(self):
        pass


class UserList(object):

    @staticmethod
    @make_decorator
    def get(last_login_start_time, last_login_end_time, register_start_time, register_end_time, **kwargs):
        # 检验最后登录日期和注册日期
        if last_login_start_time and last_login_end_time and (last_login_end_time > last_login_start_time):
            pass

        if register_start_time and register_end_time and (register_end_time > register_start_time):
            pass

        return Response(last_login_start_time, last_login_end_time, register_start_time, register_end_time, **kwargs)
