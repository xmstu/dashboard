import json

from server.cache_data import init_regions
from server.meta.decorators import make_decorator
from server.status import make_result, APIStatus, HTTPStatus
from server.utils.extend import ExtendHandler


class HeatMap(object):

    @staticmethod
    @make_decorator
    def get_result(params, data):
        # TODO 过滤参数
        if params['dimension'] == 1:
            pass

        elif params['dimension'] == 2:
            goods_list = data['goods_list']
            region_group = data['region_group'].split('.')[1]
            for detail in goods_list:
                detail[region_group] = init_regions.to_region(detail[region_group])

            ret = json.loads(json.dumps(goods_list, default=ExtendHandler.handler_to_float))

        elif params['dimension'] == 3:
            pass

        else:
            ret = [{}]

        return make_result(APIStatus.Ok, data=ret), HTTPStatus.Ok
