import calendar
import datetime
import re
import time

from server.cache_data import init_regions


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

    @staticmethod
    def handler_to_int(obj):
        """转换函数

        :param obj: 传递的函数
        :return   : Int
        """
        return obj.isoformat() if hasattr(obj, 'isoformat') else int(obj)


class Check(object):
    @staticmethod
    def is_mobile(mobile) -> bool:
        if mobile and str(mobile).isdigit():
            return bool(re.findall('1[23456789]{1}[0-9]{9}', str(mobile)))
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
            date_count[create_time] = count.get(args[0], 0)
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

    return series


def get_xAxis(periods, start_time, end_time):
    # 日期补全
    begin_date = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(start_time)), "%Y-%m-%d")
    end_date = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(end_time)), "%Y-%m-%d")

    # 日
    xAxis = []
    if periods == 2:
        date_val = begin_date
        while date_val <= end_date:
            date_str = date_val.strftime("%Y-%m-%d")
            xAxis.append(date_str)
            date_val += datetime.timedelta(days=1)

    # 周
    elif periods == 3:
        begin_flag = begin_date
        end_flag = begin_date
        count = 0

        while end_flag <= end_date:
            # 本周结束
            if count == 6:
                xAxis.append(begin_flag.strftime('%Y/%m/%d') + '-' + end_flag.strftime('%Y/%m/%d'))
                begin_flag = end_flag + datetime.timedelta(days=1)
                count = 0
            if end_flag == end_date:
                xAxis.append(begin_flag.strftime('%Y/%m/%d') + '-' + end_flag.strftime('%Y/%m/%d'))
                begin_flag = end_flag + datetime.timedelta(days=1)
                count = 0
            end_flag += datetime.timedelta(days=1)
            count += 1

    # 月
    elif periods == 4:
        begin_flag = begin_date
        end_flag = begin_date
        while end_flag <= end_date:
            month_lastweek, month_lastday = calendar.monthrange(begin_flag.year, begin_flag.month)
            # 结束日期
            if end_flag == end_date:
                xAxis.append(begin_flag.strftime('%Y/%m/%d') + '-' + end_date.strftime('%Y/%m/%d'))
            else:
                # 本月结束
                if end_flag.day == month_lastday and end_flag.month == begin_flag.month:
                    xAxis.append(begin_flag.strftime('%Y/%m/%d') + '-' + end_flag.strftime('%Y/%m/%d'))
                    begin_flag = end_flag + datetime.timedelta(days=1)
            end_flag += datetime.timedelta(days=1)

    return xAxis


def compare_time(start_time, end_time) -> bool:
    if start_time and end_time:
        if start_time <= end_time:
            return True
        else:
            return False
    elif not start_time and not end_time:
        return True
    else:
        return False


def timestamp2date(time_stamp, accuracy=1):
    if accuracy == 1:
        return time.strftime('%Y-%m-%d', time.localtime(time_stamp))
    if accuracy == 2:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_stamp))


def date2timestamp(date, accuracy=1):
    if accuracy == 1:
        return time.mktime(time.strptime(date, '%Y-%m-%d'))
    if accuracy == 2:
        return time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S'))


def date_to_timestamp(start_date, end_date):

    if not isinstance(start_date, str) and not isinstance(end_date, str):
        return start_date, end_date

    if isinstance(eval(start_date), int) and isinstance(eval(end_date), int):
        return start_date, end_date

    start_timestamp = date2timestamp(start_date, accuracy=1)
    end_timestamp = date2timestamp(end_date, accuracy=1)

    if start_timestamp != end_timestamp:
        return start_timestamp, end_timestamp
    return start_timestamp, end_timestamp + 86399


def check_region_id(region_id, locations_id):
    if region_id == 0:
        return False
    if str(region_id) in locations_id:
        return True
    parent_id = init_regions.get_parent_id(region_id)
    return check_region_id(parent_id, locations_id)
