from server.meta.decorators import make_decorator
from server.status import make_result, APIStatus, HTTPStatus


class TransportRadar(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        # TODO 过滤参数

        return make_result(APIStatus.Ok, data=data), HTTPStatus.Ok


class TransportList(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        # TODO 过滤参数

        return make_result(APIStatus.Ok, data=data), HTTPStatus.Ok