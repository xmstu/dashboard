# coding=utf-8
# author=veficos

import time
import logging

from functools import wraps, partial


class RetryExecute(Exception):
    pass


def retry_execute(count=5, *args, **kwargs):
    def wrapper(fn):
        @wraps(fn)
        def execute(*real_args, **real_kwargs):
            for _ in range(count):
                try:
                    return fn(*real_args, **real_kwargs)
                except RetryExecute:
                    continue
        return execute
    return wrapper


def performance(func=None, *args, log=logging,
                level=logging.DEBUG, message='{fn_name}: {time} (args={args}, kwargs={kwargs})', **kwargs):
    if func is None:
        return partial(performance, log=log, level=level, message=message)

    @wraps(func)
    def wrapper(*realfn_args, **realfn_kwargs):
        t0 = time.time()

        result = func(*realfn_args, **realfn_kwargs)

        interval = round(time.time() - t0, 5)

        nonlocal log

        log.log(level, message.format(fn_name=func.__str__(), time=interval, args=realfn_args, kwargs=realfn_kwargs))

        if interval >= 0.5:
            log.log(logging.ERROR,
                    'The {fn_name} function takes {time}s, please timely optimize.'.
                    format(fn_name=func.__str__(), time=interval, args=realfn_args, kwargs=realfn_kwargs))

        return result
    return wrapper


def collect_exceptions(handler, *args, **kwargs):
    def decorator(real_func):
        @wraps(real_func)
        def wrapper(*real_args, **real_kwargs):
            try:
                resp = real_func(*real_args, **real_kwargs)
                return resp
            except Exception as e:
                return handler(e, *args, func_name=real_func, **kwargs)
        return wrapper
    return decorator
