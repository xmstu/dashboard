import calendar
import datetime
import json
import time

from server.meta.decorators import make_decorator
from server.status import build_result, APIStatus, HTTPStatus, make_result
from server.utils.extend import ExtendHandler


class PromoteEffect(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        data = json.loads(json.dumps(data, default=ExtendHandler.handler_to_float))
        promote_effect_detail = data['promote_effect_detail']
        for detail in promote_effect_detail:
            detail['user_count'] = detail.get('user_count', None) or 0
            detail['wake_up_count'] = detail.get('wake_up_count', None) or 0
            detail['goods_count'] = detail.get('goods_count', None) or 0
            detail['goods_user_count'] = detail.get('goods_user_count', None) or 0
            detail['order_over_count'] = detail.get('order_over_count', None) or 0
            detail['goods_price'] = detail.get('goods_price', None) or 0
            detail['order_over_price'] = detail.get('order_over_price', None) or 0

        return build_result(APIStatus.Ok, count=data['count'], data=promote_effect_detail), HTTPStatus.Ok


class PromoteQuality(object):

    @staticmethod
    @make_decorator
    def get_result(params, data, before_promote_count):

        # 结构化数据
        date_count = {}
        for count in data:
            if count.get('create_time'):
                if count.get('count'):
                    date_count[count['create_time'].strftime('%Y-%m-%d')] = count.get('count', 0)
                elif count.get('amount'):
                    date_count[count['create_time'].strftime('%Y-%m-%d')] = count.get('amount', 0)
        # 日期补全
        begin_date = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(params['start_time'])),"%Y-%m-%d")
        end_date = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(params['end_time'])), "%Y-%m-%d")

        # 日
        xAxis = []
        series = []
        if params['periods'] == 2:
            date_val = begin_date
            while date_val <= end_date:
                date_str = date_val.strftime("%Y-%m-%d")
                date_count.setdefault(date_str, 0)
                xAxis.append(date_str)
                series.append(date_count[date_str])
                date_val += datetime.timedelta(days=1)
        # 周
        elif params['periods'] == 3:
            begin_flag = begin_date
            end_flag = begin_date
            count = 0
            sum_count = 0
            while end_flag <= end_date:
                date_str = end_flag.strftime("%Y-%m-%d")
                sum_count += date_count.get(date_str, 0)
                date_count.setdefault(date_str, sum_count)
                # 本周结束
                if count == 6:
                    xAxis.append(begin_flag.strftime('%Y/%m/%d') + '-' + end_flag.strftime('%Y/%m/%d'))
                    series.append(sum_count)
                    begin_flag = end_flag + datetime.timedelta(days=1)
                    sum_count = 0
                    count = 0
                if end_flag == end_date:
                    xAxis.append(begin_flag.strftime('%Y/%m/%d') + '-' + end_flag.strftime('%Y/%m/%d'))
                    series.append(sum_count)
                    begin_flag = end_flag + datetime.timedelta(days=1)
                    sum_count = 0
                    count = 0
                end_flag += datetime.timedelta(days=1)
                count += 1
        # 月
        elif params['periods'] == 4:
            begin_flag = begin_date
            end_flag = begin_date
            sum_count = 0
            while end_flag <= end_date:
                date_str = end_flag.strftime("%Y-%m-%d")
                sum_count += date_count.get(date_str, 0)
                month_lastweek, month_lastday = calendar.monthrange(begin_flag.year, begin_flag.month)
                # 结束日期
                if end_flag == end_date:
                    xAxis.append(begin_flag.strftime('%Y/%m/%d') + '-' + end_date.strftime('%Y/%m/%d'))
                    series.append(sum_count)
                else:
                    # 本月结束
                    if end_flag.day == month_lastday and end_flag.month == begin_flag.month:
                        xAxis.append(begin_flag.strftime('%Y/%m/%d') + '-' + end_flag.strftime('%Y/%m/%d'))
                        series.append(sum_count)
                        begin_flag = end_flag + datetime.timedelta(days=1)
                        sum_count = 0
                end_flag += datetime.timedelta(days=1)

        # 累计
        if params['dimension'] == 1 and params['data_type'] == 2:
            series = [sum(series[: i + 1]) + before_promote_count if i > 0 else series[i] + before_promote_count for i in range(len(series))]
        # 新增
        else:
            pass
        series = json.loads(json.dumps(series, default=ExtendHandler.handler_to_float))
        return make_result(APIStatus.Ok, data={'xAxis': xAxis, 'counts_series': series}), HTTPStatus.Ok