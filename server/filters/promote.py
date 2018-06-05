from server.meta.decorators import make_decorator
from server.status import build_result, APIStatus, HTTPStatus


class PromoteEffect(object):

    @staticmethod
    @make_decorator
    def get_result(data):

        return build_result(APIStatus.Ok, count=data['count'], data=data['promote_effet_detail']), HTTPStatus.Ok