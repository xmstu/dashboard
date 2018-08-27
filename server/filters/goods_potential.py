from server.meta.decorators import make_decorator
from server.status import make_result, APIStatus, HTTPStatus


class GoodsPotentialList(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        # TODO 过滤参数

        return make_result(APIStatus.Ok), HTTPStatus.Ok