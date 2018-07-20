from server.meta.decorators import make_decorator
from server.status import make_result, APIStatus, HTTPStatus
from server.utils.extend import get_struct_data


class PriceTrend(object):

    @staticmethod
    @make_decorator
    def get_result(params, data):
        price_trend = data.get('price_trend', [])
        # 按日
        # xAxis = []
        price_trend_series = []
        avg_price = []
        for detail in price_trend:
            if detail.get('create_time'):
                create_time = detail['create_time']
                # xAxis.append(create_time)
                trend_series = [detail.get('max_price', 0), detail.get('min_price', 0)] * 2
                price_trend_series.append([create_time] + trend_series)
                avg_price.append(detail.get('avg_price', 0))

        ret = {
            # "xAxis": xAxis,
            "price_trend_series": price_trend_series,
            "avg_price": avg_price,
            "recommend_price_one": data.get("recommend_price_one", 0),
            "recommend_price_two": data.get("recommend_price_two", 0)
        }

        return make_result(APIStatus.Ok, data=ret), HTTPStatus.Ok