from server.meta.decorators import make_decorator
from server.status import make_result, APIStatus, HTTPStatus
from server.utils.extend import get_struct_data


class PriceTrend(object):

    @staticmethod
    @make_decorator
    def get_result(params, data):
        # TODO 过滤参数
        # 按日，按月，按年
        xAxis, price_trend_series = get_struct_data(data['price_trend'], params, 'max_price', 'min_price')

        ret = {
            "xAxis": xAxis,
            "price_trend_series": price_trend_series,
            "recommend_price_one": data.get("recommend_price_one", 0),
            "recommend_price_two": data.get("recommend_price_two", 0)
        }

        return make_result(APIStatus.Ok, data=ret), HTTPStatus.Ok