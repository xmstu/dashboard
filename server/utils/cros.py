# coding=utf-8
# author=veficos
from functools import wraps
from flask import make_response, jsonify
from flask_restplus.cors import crossdomain
allow_cross_domain = crossdomain


def allow_cross_domain_ex(origin='*', methods=None, headers=None):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)

    def cross_domain(fun):
        @wraps(fun)
        def wrapper_fun(*args, **kwargs):
            rst = fun(*args, **kwargs)
            rst.headers['Access-Control-Allow-Origin'] = origin
            rst.headers['Access-Control-Allow-Methods'] = methods
            # allow_headers = "Referer,Accept,Origin,User-Agent"
            rst.headers['Access-Control-Allow-Headers'] = headers
            return rst
        return wrapper_fun
    return cross_domain
