import calendar
import datetime
import re
import time


class ExtendHandler(object):
    """扩展类

    """

    @staticmethod
    def handler(obj):
        """转换函数

        :param obj: 传递的函数
        :return   : String
        """
        return obj.isoformat() if hasattr(obj, 'isoformat') else str(obj)

    @staticmethod
    def handler_to_float(obj):
        """转换函数

        :param obj: 传递的函数
        :return   : Float
        """
        return obj.isoformat() if hasattr(obj, 'isoformat') else float(obj)


class Check(object):
    @staticmethod
    def is_mobile(mobile) -> bool:
        if mobile and str(mobile).isdigit():
            return bool(re.findall('1[23456789]{1}['
                                   '0-9]{9}', str(mobile)))
        return False


def get_struct_data(data, params, *args, **kwargs):
    """
    结构化结果，按日，按周，按月
    :param data: 从数据库获取到的数据
    :param params: 查询参数
    :param args:
    :param kwargs:
    :return: xAxis, series
    """

    # 结构化数据
    date_count = {}
    for count in data:
        if count.get('create_time'):
            create_time = count['create_time'].strftime('%Y-%m-%d') if isinstance(count['create_time'], int) else count['create_time']
            date_count[create_time] = count.get('count', 0)
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

    return xAxis, series