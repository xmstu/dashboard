import calendar
import datetime
import hashlib
import re
import time
import math

from server.cache_data import init_regions
from server.utils.constant import weekdays


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


class ParamsError(Exception):
    def __init__(self, *args, **kwargs):
        pass


def complement_time(start_time, end_time):
    if start_time and not end_time:
        end_time = int(time.time())
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


def get_previous_week_day(dayname, now_date=None):
    try:
        if now_date is None:
            now_date = datetime.datetime.today()
        elif isinstance(now_date, datetime.datetime):
            pass
        elif isinstance(now_date, str):
            now_date = datetime.datetime.strptime(now_date, "%Y-%m-%d")
        else:
            raise Exception("date must be datetime cls or str cls")
        day_num = now_date.weekday()
        day_num_target = weekdays.index(dayname)
        days_ago = (7 + day_num - day_num_target) % 7
        if days_ago == 0:
            days_ago = 7
        target_date = now_date - datetime.timedelta(days=days_ago)
        return target_date
    except Exception as e:
        print("获取之前的日期失败,错误原因是 [error: %s]" % e)


def get_previous_month_last_day(now_date):
    try:
        if now_date is None:
            now_date = datetime.datetime.today()
        elif isinstance(now_date, datetime.datetime):
            pass
        elif isinstance(now_date, str):
            now_date = datetime.datetime.strptime(now_date, "%Y-%m-%d")
        else:
            raise Exception("date must be datetime cls or str cls")
        if now_date.month == 1:
            last_date_month = 12
            last_date_year = now_date.year - 1
        else:
            last_date_month = now_date.month - 1
            last_date_year = now_date.year
        _, last_month_end_days = calendar.monthrange(last_date_year, last_date_month)
        return datetime.datetime(last_date_year, last_date_month, last_month_end_days, 23, 59, 59)
    except Exception as e:
        print("获取之前的日期失败,错误原因是 [error: %s]" % e)


def get_last_month_date(start_date, end_date):
    last_month_end_day = end_date
    while True:
        last_month_end_day = get_previous_month_last_day(last_month_end_day)
        if last_month_end_day.month > start_date.month or last_month_end_day.year > start_date.year:
            last_month_start_day = datetime.datetime(last_month_end_day.year, last_month_end_day.month, 1)
            yield last_month_start_day, last_month_end_day
        else:
            last_month_start_day = datetime.datetime(last_month_end_day.year, last_month_end_day.month, 1)
            yield last_month_start_day, last_month_end_day
            break


def get_last_week_date(start_date, end_date):
    start_date_weekend = datetime.datetime(start_date.year, start_date.month, start_date.day+(6-start_date.weekday()))

    last_week_start_day = end_date
    if last_week_start_day.weekday() != 0:
        last_week_start_day = get_previous_week_day("Monday", last_week_start_day)
    last_week_end_day = end_date

    while True:
        last_week_start_day = get_previous_week_day("Monday", last_week_start_day)
        last_week_end_day = get_previous_week_day("Sunday", last_week_end_day)
        if last_week_end_day >= start_date_weekend:
            last_week_end_day = datetime.datetime(last_week_end_day.year, last_week_end_day.month, last_week_end_day.day, 23, 59, 59)
            yield last_week_start_day, last_week_end_day
        else:
            break

