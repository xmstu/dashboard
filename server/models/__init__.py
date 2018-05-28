# coding=utf-8
# author=qiao
import functools

from server import log
from server.db.db_orm import MetaModel


def catch_exception_log(name):
    def accept_func(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                log.debug("%s, arg=%s kwarg=%s" % (name, args[1:], kwargs))
                result = func(*args, **kwargs)
                log.debug("%s result=%s" % (name, result))
                return result
            except Exception as e:
                log.warn(name, exc_info=True)
                raise e

        return wrapper

    return accept_func


class BaseModel(metaclass=MetaModel):

    pass


class ReadORMModel(object):

    """
    虚拟的只读类,在多继承 时欺骗编译器
    """

    @staticmethod
    def query_one(cursor, **payload):
        return {}

    @staticmethod
    def query_count(cursor, **payload):
        return 1

    @staticmethod
    def query_exists(cursor, **payload):
        return True

    @staticmethod
    def query(cursor, **payload):
        return []

    @staticmethod
    def query_paging(cursor, index, count, order_by, **payload):
        return []


class WriteORMModel(object):
    """
    虚拟的写入类,在多继承 时欺骗编译器
    """

    @staticmethod
    def delete(cursor, **payload):
        return 1

    @staticmethod
    def update(cursor, fields, **payload):
        return 1

    @staticmethod
    def insert(cursor, payload):
        return 1


