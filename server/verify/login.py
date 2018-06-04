
from flask_restful import abort

from server.meta.decorators import make_decorator, Response
from server.status import make_result, HTTPStatus, APIStatus


class LoginSetting(object):

    @staticmethod
    @make_decorator
    def post(user_name, password, role):
        if user_name and password and role:
            return Response(user_name=user_name, password=password, role=role)

        abort(HTTPStatus.NotFound, **make_result(status=APIStatus.NotFound))


