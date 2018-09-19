import calendar
import datetime
import hashlib
import re
import time
import math

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
    if params.get('periods') == 2:
        date_val = begin_date
        while date_val <= end_date:
            date_str = date_val.strftime("%Y-%m-%d")
            date_count.setdefault(date_str, 0)
            xAxis.append(date_str)
            series.append(date_count[date_str])
            date_val += datetime.timedelta(days=1)

    # 周
    elif params.get('periods') == 3:
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
    elif params.get('periods') == 4:
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


class ParamsError(Exception):
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


def complement_time(start_time, end_time):
    if start_time and not end_time:
        end_time = time.time()
        if start_time <= end_time:
            return start_time, end_time
        else:
            raise ParamsError
    elif not start_time and end_time:
        start_time = int(time.time() - 86400 * 7)
        if start_time <= end_time:
            return start_time, end_time
        else:
            raise ParamsError
    else:
        return start_time, end_time


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


def interval_time_to_format_time(interval_time):
    format_time = (str(int(interval_time / 3600)) + '小时' if int(
        interval_time / 3600) > 0 else '') + \
                (str(int(interval_time % 3600 / 60)) + '分' if int(
                    interval_time % 3600 / 60) > 0 else '') + \
                (str(int(interval_time % 3600 % 60)) + '秒' if int(
                    interval_time % 3600 % 60) > 0 else '')

    return format_time


def check_region_id(region_id, locations_id):
    if region_id == 0:
        return False
    if str(region_id) in locations_id:
        return True
    parent_id = init_regions.get_parent_id(region_id)
    return check_region_id(parent_id, locations_id)


class CarPrice(object):
    _fast = tuple()
    _distance = 0

    def __init__(self, a, b, c, d, e):
        self._fast = (a, b, c, d)
        self._distance = e

    def __str__(self):
        return 'CarPrice(%s, %s)' % (self._fast, self._distance)

    # 是否在价格区间
    def is_between(self, distance):
        # [25, 400)
        if 25 <= distance <= self._distance:
            return True
        else:
            return False

    # 获取快车价格
    def get_fast_price(self, d):
        # y=ax+bx^2+cx^3+d
        return int(self._fast[0] * d + self._fast[1] * math.pow(d, 2) + self._fast[2] * math.pow(d, 3) + self._fast[3])


data_price = {
    # =26.38+2.54*A2+(-4.3)*(10^-3)*A2^2+6.44*(10^-6)*A2^3
    '小面包车': [CarPrice(2.54, -4.3/1000, 0.00000644, 26.38, 30), 1.05],
    # =28.79+2.8*A3+(-3.85)*(10^-3)*A3^2+4.56*(10^-6)*A3^3
    '中面包车': [CarPrice(2.8, -3.85/1000, 0.00000456, 28.79, 30), 1.2],
    # =28.08+3.18*A3+(-4.84)*(10^-3)*A3^2+5.37*(10^-6)*A3^3
    '小货车': [CarPrice(3.18, -4.84/1000, 0.00000537, 28.08, 30), 1.2],
    # =55.17+3.96*A3+(-3.9)*(10^-3)*A3^2+5.21*(10^-6)*A3^3
    '4.2米': [CarPrice(3.96, -3.9/1000, 0.00000521, 55.17, 30), 1.17],
    # =1.04*(10^2)+4.52*A3-2.28*(10^-3)*A3^2
    '5.2米': [CarPrice(4.52, -2.28/1000, 0, 104, 30), 1.12],
    # =2.25*(10^2)+3.7*A3+2.52*(10^-3)*A3^2-1.85*(10^-6)*A3^3
    '6.8米': [CarPrice(3.7, 2.52/1000, -0.00000185, 225, 30), 1.1],
    # =2.07*(10^2)+4.77*A4+(-1.45)*(10^-3)*A4^2+2.01*(10^-6)*A4^3
    '7.6米': [CarPrice(4.77, -1.45/1000, 0.00000201, 207, 30), 1.1],
    # =3.29*(10^2)+6.88*A3+(-1.91)*(10^-3)*A3^2+5.84*(10^-7)*A3^3
    '9.6米': [CarPrice(6.88, -1.91/1000, 0.000000584, 329, 30), 1.1],
    # =6.56*(10^2)+9.88*A2-6.26*(10^-3)*A2^2
    '13米': [CarPrice(9.88, -6.26/1000, 0, 656, 30), 1],
    # =1.02*(10^3)+11.2*A2-7.48*(10^-3)*A2^2
    '17.5米': [CarPrice(11.2, -7.48/1000, 0, 1020, 30), 1],
}


def hash_str(word):
    m2 = hashlib.md5()
    m2.update(word.encode("utf-8"))
    return m2.hexdigest()


def pwd_to_hash(user_name, pwd):

    return hash_str(user_name+pwd+'sshtc')
