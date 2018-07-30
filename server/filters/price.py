import time
from itertools import groupby
from operator import itemgetter

from server.meta.decorators import make_decorator
from server.status import make_result, APIStatus, HTTPStatus
from server.utils.extend import data_price


class PriceTrend(object):

    @staticmethod
    @make_decorator
    def get_result(params, data):
        price_trend = data.get('price_trend', [])
        # # 按日
        # date_count = {}
        # date_val = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(params['start_time'])), "%Y-%m-%d")
        # end_date = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(params['end_time'])), "%Y-%m-%d")
        # for detail in price_trend:
        #     if detail.get('create_time'):
        #         create_time = detail['create_time']
        #         trend_series = [create_time] + [detail.get('max_price', 0), detail.get('min_price', 0)] * 2 + [detail.get('avg_price', 0)]
        #         date_count[create_time] = trend_series
        #
        # while date_val <= end_date:
        #     date_str = date_val.strftime("%Y-%m-%d")
        #     date_count.setdefault(date_str, [date_str, 0, 0, 0, 0, 0])
        #     date_val += datetime.timedelta(days=1)
        #
        # price_trend_series = list(date_count.values())
        #
        # price_trend_series.sort(key=lambda k: time.mktime(time.strptime(k[0], '%Y-%m-%d')))
        #
        # avg_price = [i.pop() for i in price_trend_series]
        #
        # ret = {
        #     "price_trend_series": price_trend_series,
        #     "avg_price": avg_price,
        #     "recommend_price_one": data.get("recommend_price_one", 0),
        #     "recommend_price_two": data.get("recommend_price_two", 0)
        # }

        recommend_price_instance = data_price[params['vehicle_length']]
        # 从后往前删，避免发生元素顶位的问题
        for detail in price_trend[::-1]:
            detail_recommend_price = recommend_price_instance.get_fast_price(detail.get('mileage_total'))
            if not (0.6 * detail_recommend_price < detail['price'] < 2 * detail_recommend_price) and not (detail['price'] < 1000000):
                price_trend.remove(detail)

        result = {}
        avg_mileage_list = []
        price_trend.sort(key=itemgetter('create_time', 'price'))

        # 用外部指针记录迭代次数
        index = 0
        last_date_str = ''
        for date_str, item in groupby(price_trend, key=itemgetter('create_time')):
            price = []
            mileage = []
            for detail in item:
                price.append(detail['price'])
                mileage.append(detail['mileage_total'])
            max_price, min_price = max(price), min(price)
            avg_price = float(('%.2f' % (sum(price) / len(price))))
            avg_mileage = sum(mileage) / len(mileage)
            avg_mileage_list.append(avg_mileage)

            result[date_str] = [date_str, min_price, max_price, result[last_date_str][-1] if index - 1 >= 0 else 0, avg_price]
            index += 1
            last_date_str = date_str

        price_trend_series = [i for i in result.values()]
        avg_price_list = [i[-1] for i in result.values()]
        # 获取价格基准线
        recommend_price_one = recommend_price_instance.get_fast_price(params['min_mileage'])
        recommend_price_two = recommend_price_instance.get_fast_price(params['max_mileage'])
        if price_trend:
            if params.get('from_province_id') and params.get('to_province_id'):
                avg_mileage = sum(avg_mileage_list) / len(avg_mileage_list)
                recommend_price_one = recommend_price_two = recommend_price_instance.get_fast_price(avg_mileage)
        else:
            recommend_price_one = 0
            recommend_price_two = 0

        ret = {
            'price_trend_series': price_trend_series,
            'avg_price': avg_price_list,
            'recommend_price_one': recommend_price_one,
            'recommend_price_two': recommend_price_two
        }

        return make_result(APIStatus.Ok, data=ret), HTTPStatus.Ok
