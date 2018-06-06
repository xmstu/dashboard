import datetime
import time

from server.meta.decorators import make_decorator
from server.status import build_result, APIStatus, HTTPStatus, make_result


class PromoteEffect(object):

    @staticmethod
    @make_decorator
    def get_result(data):

        return build_result(APIStatus.Ok, count=data['count'], data=data['promote_effet_detail']), HTTPStatus.Ok


class PromoteQuality(object):

    @staticmethod
    @make_decorator
    def get_result(params, data):
        # 结构化数据
        date_count = {}
        for count in data:
            if count['create_time']:
                date_count[count['create_time']] = count.get('count', 0)
        # 日期补全
        begin_date = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(params['start_time'])),
                                                "%Y-%m-%d")
        end_date = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(params['end_time'])), "%Y-%m-%d")
        date_val = begin_date
        date_list = {}
        while date_val <= end_date:
            date_str = date_val.strftime("%Y-%m-%d")
            date_list[date_str] = date_count.get(date_str, 0)
            date_val += datetime.timedelta(days=1)
        # 日
        xAxis = []
        series = []
        if params['periods'] == 2:
            for i, j in date_list.items():
                xAxis.append(i)
                series.append(j)
        # 周
        elif params['periods'] == 3:
            date_str = '%(begin)s到%(end)s'
            start_val = begin_date
            end_val = begin_date
            sum_count = 0
            while end_val <= end_date:
                if begin_date == end_val:
                    sum_count += date_list[end_val.strftime("%Y-%m-%d")]
                elif begin_date.isoweekday() != end_val.isoweekday():
                    sum_count += date_list[end_val.strftime("%Y-%m-%d")]
                elif begin_date.isoweekday() == end_val.isoweekday():
                    xAxis.append(date_str % {
                        'begin': start_val.strftime("%Y-%m-%d"),
                        'end': end_val.strftime("%Y-%m-%d")
                    })
                    series.append(sum_count)
                    start_val = end_val
                    sum_count = 0

                if start_val == end_date and end_val.isoweekday() != end_date.isoweekday():
                    xAxis.append(date_str % {
                        'begin': start_val.strftime("%Y-%m-%d"),
                        'end': end_date.strftime("%Y-%m-%d")
                    })
                    series.append(sum_count)

                end_val += datetime.timedelta(days=1)

        return make_result(APIStatus.Ok, data={'xAxis': xAxis, 'series': series}), HTTPStatus.Ok