# coding=utf-8
# author=veficos

from functools import wraps, partial


class PassingParameterError(Exception):
    pass


class PassingCalledError(Exception):
    pass


class Finale(tuple):
    def __new__(cls, *args):
        return super(Finale, cls).__new__(cls, args)

    def __repr__(self):
        return super(Finale, self).__repr__()

    def __str__(self):
        return super(Finale, self).__repr__()


class Passing(dict):
    # 将字典数据结构化
    # p = Passing(args = {'mobile': '15917907641', 'code': '3591'})
    # p -> {'args': {'mobile': '15917907641', 'code': '3591'}}
    def __init__(self, level=None, **kwargs):
        self.level = level
        super(Passing, self).__init__(**kwargs)

    def __str__(self):
        # 面向用户的显示
        return super(Passing, self).__str__()

    def __repr__(self):
        # 面向程序员的显示
        return super(Passing, self).__repr__()


def __collect_prevfunc_params(**params):
    restrictions = {}
    values = {}
    for name in params:
        typ = params[name]
        try:
            isinstance(0, typ)
            restrictions.update({name: typ})
        except:
            values.update({name: typ})
    level = values.pop('level', None)
    return restrictions, values, level


def __check_params(restrictions, values, next_func, params):
    next_params = {}
    for k in restrictions:
        value = params.get(k, None)
        if value is None:
            raise PassingCalledError("{func_name} missing 1 required positional argument: {key}".
                                     format(func_name=next_func.__name__, key=k))
        if not isinstance(value, restrictions[k]):
            raise PassingParameterError('{key} must be a {typ}'.
                                        format(key=k, typ=restrictions[k].__name__))
        next_params[k] = value
    next_params.update(values)
    return next_params


def __wrapper_response(restrictions, values, next_func, resp):
    if isinstance(resp, Finale):
        if not resp:
            return None
        if len(resp) == 1:
            return resp[0]
        return resp

    elif isinstance(resp, Passing):
        result = next_func(**__check_params(restrictions, values, next_func, resp))
        return result


def make_passing(next_func=None, level=None):
    if next_func is None:
        return partial(make_passing, level=level)

    def input_params(**params):
        restrictions, values, decorator_func_level = __collect_prevfunc_params(**params)
        real_func_level = decorator_func_level if decorator_func_level else level

        def decorator(real_func):
            @wraps(real_func)
            def wrapper(*real_args, **real_kwargs):
                resp = real_func(*real_args, **real_kwargs)
                if isinstance(resp, Finale):
                    if not resp:
                        return None
                    if len(resp) == 1:
                        return resp[0]
                    return resp
                elif isinstance(resp, Passing):
                    if real_func_level and resp.level:
                        if real_func_level > resp.level:
                            return resp
                    result = next_func(**__check_params(restrictions, values, next_func, resp))
                    if isinstance(result, Finale):
                        if not result:
                            return None
                        if len(result) == 1:
                            return result[0]
                    return result
                else:
                    return resp

            return wrapper

        return decorator

    return input_params


if __name__ == '__main__':
    import time
    import logging

    def fn_performance(*args, **kwargs):
        def wrapper(real_fn):
            @wraps(real_fn)
            def function_timer(*realfn_args, **realfn_kwargs):
                t0 = time.time()

                result = real_fn(*realfn_args, **realfn_kwargs)

                t1 = time.time()

                if not args and not kwargs:
                    logging.warning('{fn_name}: {time}'.format(fn_name=real_fn.__name__, time=round(t1 - t0, 5)))

                if args:
                    if len(args) > 1:
                        raise TypeError(
                            'fn_performance() takes 1 positional arguments but %s were given' % (len(args),))
                    else:
                        [fn(real_fn, t1 - t0) for fn in args]

                log = kwargs.get('log', None)
                if log:
                    log.warning('{fn_name}: {time}'.format(fn_name=real_fn.__name__, time=round(t1 - t0, 5)))

                return result

            return function_timer

        return wrapper

    def collect_exception(handler, *args, **kwargs):
        def decorator(real_func):
            @wraps(real_func)
            def wrapper(*real_args, **real_kwargs):
                try:
                    last_result = real_func(*real_args, **real_kwargs)
                    return last_result
                except Exception as e:
                    return handler(e, *args, **kwargs)

            return wrapper

        return decorator

    def decorator_performance():
        def d4(f):
            def d(*args, **kwargs):
                return ','.join(['d4()', f(*args, **kwargs)])

            return d

        def d3(f):
            def d(*args, **kwargs):
                return ','.join(['d3()', f(*args, **kwargs)])

            return d

        def d2(f):
            def d(*args, **kwargs):
                return ','.join(['d2()', f(*args, **kwargs)])

            return d

        @d4
        @d3
        @d2
        def d1(a):
            return ','.join(['d1()', a])

        print(d1(a='a'))

        @fn_performance(log=logging)
        def pf():
            for _ in range(1000000):
                d1(a='a')

        pf()

        @fn_performance(log=logging)
        def times():
            t = time.time()
            i = 0
            while True:
                s = time.time()
                if s - t >= 1:
                    break
                d1(a='a')
                i += 1
            print('d1: ', i, s)

        times()

    def call_performance():
        def f4(a):
            return ','.join([a, 'f4()'])

        def f3(a):
            return ','.join([f4(a), 'f3()'])

        def f2(a):
            return ','.join([f3(a), 'f2()'])

        def f1(a):
            return ','.join([f2(a), 'f1()'])

        print(f1(a='a'))

        @fn_performance(log=logging)
        def pf():
            for _ in range(1000000):
                f1(a='a')

        pf()

        @fn_performance(log=logging)
        def times():
            t = time.time()
            i = 0
            while True:
                s = time.time()
                if s - t >= 1:
                    break
                f1(a='a')
                i += 1
            print('f1: ', i, s - t)

        times()

    def passing_performance():
        @make_passing(level=3)
        def p4(b):
            return ','.join(['p4()', b])

        @make_passing(level=4)
        def p3(a):
            return Passing(level=1, b=','.join(['p3()', a]))

        @make_passing(level=5)
        def p2(a):
            return Passing(level=2, a=','.join(['p2()', a]))

        @p4(level=1, b=str)
        @p3(level=2, a=str)
        @p2(level=4, a=str)
        def p1(a):
            return Passing(level=4, a=','.join(['p1()', a]))

        print(p1('a'))

        @fn_performance(log=logging)
        def pf():
            for _ in range(1000000):
                p1(a='a')

        pf()

        @fn_performance(log=logging)
        def times():
            t = time.time()
            i = 0
            while True:
                s = time.time()
                if s - t >= 1:
                    break
                p1(a='a')
                i += 1
            print('p1: ', i, s - t)

        times()

    def without_params_passing_performance():
        @make_passing
        def p4():
            return Finale()

        @make_passing
        def p3():
            return Passing()

        @make_passing
        def p2():
            return Passing()

        @p4()
        @p3()
        @p2()
        def p1():
            return Passing()

        print(p1())

        @fn_performance(log=logging)
        def pf():
            for _ in range(1000000):
                p1()

        pf()

        @fn_performance(log=logging)
        def times():
            t = time.time()
            i = 0
            while True:
                s = time.time()
                if s - t >= 1:
                    break
                p1()
                i += 1
            print('p1: ', i, s - t)

        times()

    def for_performance():
        @fn_performance(log=logging)
        def p():
            for _ in range(1000000):
                pass

        p()

        @fn_performance(log=logging)
        def times():
            t = time.time()
            i = 0
            while True:
                s = time.time()
                if s - t >= 1:
                    break
                i += 1
            print('p1: ', i, s - t)

        times()

    for_performance()
    call_performance()
    decorator_performance()
    without_params_passing_performance()
    passing_performance()
