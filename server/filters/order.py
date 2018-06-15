from server.meta.decorators import make_decorator
from server.status import make_result, APIStatus, HTTPStatus


class OrdersReceivedStatistics(object):

    @staticmethod
    @make_decorator
    def get_result(data):

        return make_result(APIStatus.Ok, data=data), HTTPStatus.Ok
