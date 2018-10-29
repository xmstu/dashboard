import hashlib
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
    return hash_str(user_name + pwd + 'sshtc')
