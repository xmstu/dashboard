from server.meta.decorators import make_decorator
from server.status import build_result, APIStatus, HTTPStatus


class GoodsList(object):

    @staticmethod
    @make_decorator
    def get_result(goods_list):

        goods_count = goods_list['goods_count']
        goods_detail = goods_list['goods_detail']
        # TODO 过滤参数
        pass

        return build_result(APIStatus.Ok, count=goods_count, data=goods_detail), HTTPStatus.Ok