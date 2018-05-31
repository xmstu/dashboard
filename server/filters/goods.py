from server.meta.decorators import make_decorator
from server.status import build_result, APIStatus, HTTPStatus


class GoodsList(object):

    @staticmethod
    @make_decorator
    def get_result(data):

        goods_detail = data['goods_detail']
        # TODO 过滤参数
        for detail in goods_detail:
            goods_standard = []
            if detail['NAME']:
                goods_standard.append(detail['NAME'])
            if detail['weight']:
                goods_standard.append(detail['weight'])
            if detail['volume']:
                goods_standard.append(detail['volume'])
            detail['goods_standard'] = ','.join(goods_standard) if goods_standard else '没有规格'
            detail.pop('NAME')
            detail.pop('weight')
            detail.pop('volume')

        return build_result(APIStatus.Ok, count=data['goods_count'], data=goods_detail), HTTPStatus.Ok