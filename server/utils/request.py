# coding=utf-8
# author=veficos

import html

from flask_restful import abort
from flask_restful import request
from server.status import APIStatus, HTTPStatus, make_result


def payload_escape(payload):
    for k in payload:
        if isinstance(payload[k], str):
            payload[k] = html.escape(payload[k])
        elif isinstance(payload[k], dict):
            payload[k] = payload_escape(payload[k])
    return payload


def get_payload():
    """获取post参数"""
    payload = request.json
    if payload:
        return payload_escape(payload)
    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='缺少请求数据'))


def get_arg(key, default=None):
    """获取get参数"""
    value = request.args.get(key, default)
    if value is not None:
        return value
    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='缺少请求参数%s' % key))


def get_arg_int(key, default=None):
    value = request.args.get(key, default)
    if str(value).lstrip('-').isdigit():
        return int(value)
    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数 %s 不是 int' % (key,)))


def get_all_arg():
    # request.args ImmutableMultiDict 是不可变的
    return request.args.to_dict()
