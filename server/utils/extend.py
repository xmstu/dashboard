import calendar
import datetime
import hashlib
import re
import time

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

