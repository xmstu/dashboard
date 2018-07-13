from server.meta.decorators import make_decorator
from server.status import make_result, APIStatus, HTTPStatus
from server.utils.extend import get_xAxis, get_struct_data


class PriceTrend(object):

    @staticmethod
    @make_decorator
    def get_result(params, data):
        # TODO 过滤参数
        # 按日，按月，按年
        xAxis = get_xAxis(params['periods'], params['start_time'], params['end_time'])
        price_trend_series = get_struct_data(data['price_trend'], params, 'max_price', 'min_price')

        ret = {
            "xAxis": xAxis,
            "price_trend_series": price_trend_series
        }

        return make_result(APIStatus.Ok, data=ret), HTTPStatus.Ok