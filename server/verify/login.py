
from flask_restful import abort

from server.meta.decorators import make_decorator, Response
from server.status import make_result, HTTPStatus, APIStatus


class LoginSetting(object):

    @staticmethod
    @make_decorator
    def post(user_name, password, role):
        if role and role not in (1, 4):
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='角色选择错误'))
        if user_name and password:
            return Response(user_name=user_name, password=password, role=role)

        abort(HTTPStatus.NotFound, **make_result(status=APIStatus.NotFound))


