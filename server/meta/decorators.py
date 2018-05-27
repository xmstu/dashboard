# coding=utf-8
# author=veficos

import functools
from .errors import *

# 封装字典，flask_restplus返回对象
class Response(dict):
    def __init__(self, *args, **kwargs):
        super(Response, self).__init__(*args, **kwargs)

# 封装装饰器
def make_decorator(f):
    def input_params(**params):
        restriction = {}
        values = {}
        for name in params:
            typ = params[name]
            try:
                isinstance(0, typ)
                restriction.update({name: typ})
            except:
                values.update({name: typ})

        def accept_func(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                last_result = func(*args, **kwargs)
                if not isinstance(last_result, Response):
                    raise ResponseError('the {func_name} return value must be a Response'.format(func_name=func.__name__))

                next_params = {}
                for k in restriction:
                    value = last_result.get(k, None)
                    if value is None:
                        raise ResponseError("{func_name} missing 1 required positional argument: {key}".format(func_name=f.__name__, key=k))

                    if not isinstance(value, restriction[k]):
                        raise ParameterError('{key} must be a {typ}'.format(key=k, typ=restriction[k].__name__))
                    next_params[k] = value

                if values:
                    next_params.update(values)
                return f(**next_params)
            return wrapper
        return accept_func

    return input_params


def catch_exception(handler):
    def accept_func(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                handler(e)
        return wrapper
    return accept_func

if __name__ == '__main__':
    g = {
        'a': 10,
        'b': 20
    }

    def decorator(g, shit, bitch):
        print(g, shit, bitch)
        return Response(a=g['a'], b=g['b'])

    fuck_the_world = make_decorator(decorator)

    @fuck_the_world(g=g, shit=str, bitch=str)
    def flat_func():
        return Response(shit= 'shit', bitch= 'bitch')

    print(flat_func())
