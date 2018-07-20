import datetime
import time

from server.meta.decorators import make_decorator
from server.status import make_result, APIStatus, HTTPStatus


class PriceTrend(object):

    @staticmethod
    @make_decorator
    def get_result(params, data):
        price_trend = data.get('price_trend', [])
        # 按日
        date_count = {}
        date_val = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(params['start_time'])), "%Y-%m-%d")
        end_date = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(params['end_time'])), "%Y-%m-%d")
        for detail in price_trend:
            if detail.get('create_time'):
                create_time = detail['create_time']
                trend_series = [detail.get('max_price', 0), detail.get('min_price', 0)] * 2
                date_count[create_time] = [create_time] + trend_series + [detail.get('avg_price', 0)]

        while date_val <= end_date:
            date_str = date_val.strftime("%Y-%m-%d")
            date_count.setdefault(date_str, [date_str, 0, 0, 0, 0, 0])
            date_val += datetime.timedelta(days=1)

        price_trend_series = list(date_count.values())

        price_trend_series.sort(key=lambda k: time.mktime(time.strptime(k[0], '%Y-%m-%d')))

        avg_price = [i.pop() for i in price_trend_series]

        ret = {
            "price_trend_series": price_trend_series,
            "avg_price": avg_price,
            "recommend_price_one": data.get("recommend_price_one", 0),
            "recommend_price_two": data.get("recommend_price_two", 0)
        }

        return make_result(APIStatus.Ok, data=ret), HTTPStatus.Ok
