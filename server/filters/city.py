from server.meta.decorators import make_decorator
from server.status import build_result, HTTPStatus, APIStatus


class CityOrderListFilterDecorator(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        # TODO 过滤参数

        return build_result(APIStatus.Ok, count=data['order_counts'], data=data['order_detail']), HTTPStatus.Ok
