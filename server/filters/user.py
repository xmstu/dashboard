import json

from server.meta.decorators import make_decorator
from server.status import build_result, HTTPStatus, APIStatus


class UserList(object):

    @staticmethod
    @make_decorator
    def get(user_list):
        user_list = json.loads(json.dumps(user_list))

        return build_result(APIStatus.Ok, data=user_list), HTTPStatus.Ok