
from server import log
from server.meta.decorators import make_decorator, Response
from flask_restful import abort
from server.status import make_result, HTTPStatus, APIStatus

class LoginSetting(object):

    @staticmethod
    @make_decorator
    def post(user_name, password):
        if user_name and password:
            return Response(user_name=user_name, password=password)

        abort(HTTPStatus.NotFound, **make_result(status=APIStatus.NotFound))


