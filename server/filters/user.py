import json

from server.meta.decorators import make_decorator
from server.status import build_result, HTTPStatus, APIStatus, make_result
import datetime, time, calendar
from functools import reduce

class UserList(object):

    @staticmethod
    @make_decorator
    def get(user_list):
        # 过滤字段
        user_list = json.loads(json.dumps(user_list))
        user_detail = user_list['user_detail']
        for detail in user_detail:
            # 认证
            role_auth = []
            if detail['auth_goods']:
                role_auth.append('货主')
            if detail['auth_driver']:
                role_auth.append('司机')
            if detail['auth_company']:
                role_auth.append('物流公司')
            detail['role_auth'] = ','.join(role_auth) if role_auth else '未认证'
            detail.pop('auth_goods')
            detail.pop('auth_driver')
            detail.pop('auth_company')

            detail['usual_city'] = detail['usual_city'] if detail['usual_city'] else ''

        return build_result(APIStatus.Ok, count=user_list['user_count'], data=user_detail), HTTPStatus.Ok


class UserStatistic(object):

    @staticmethod
    @make_decorator
    def get_result(params, data, before_user_count):
        # 结构化数据
        date_count = {}
        for count in data:
            if count['create_time']:
                date_count[count['create_time'].strftime('%Y-%m-%d')] = count.get('count', 0)
        # 日期补全
        begin_date = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(params['start_time'])), "%Y-%m-%d")
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

        # 新增
        if params['user_type'] == 1:
            pass
        # 累计
        else:
            series = [sum(series[: i+1]) + before_user_count if i > 0 else series[i] + before_user_count for i in range(len(series))]
        return make_result(APIStatus.Ok, data={'xAxis': xAxis, 'series': series}), HTTPStatus.Ok