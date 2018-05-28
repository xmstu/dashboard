# coding=utf-8
# author=veficos

import html

from flask import session

from flask_restful import abort
from flask_restful import request

from server.status import APIStatus, HTTPStatus, make_result


def get_ip():
    return request.headers.get('X-Real-IP') or request.remote_addr


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ('xls',)


def get_file(filename):
    return request.get_array(field_name=filename)


def payload_escape(payload):
    """
    " -> &quot;
    """
    for k in payload:
        if isinstance(payload[k], str):
            payload[k] = html.escape(payload[k])
        elif isinstance(payload[k], dict):
            payload[k] = payload_escape(payload[k])
    return payload


def payload_unescape(payload):
    """
    &quot; -> "
    """
    for k in payload:
        if isinstance(payload[k], str):
            payload[k] = html.unescape(payload[k])
        elif isinstance(payload[k], dict):
            payload[k] = payload_unescape(payload[k])
    return payload


def get_token():
    token = request.headers.get('token', None)
    if token:
        return token
    abort(HTTPStatus.UnAuthorized, **make_result(status=APIStatus.UnLogin, msg='用户已下线，请重新登陆'))


def get_session():
    if "login" in session:
        return {"id": session["login"]["id"], "role": session["login"]["role"]}
    abort(HTTPStatus.UnAuthorized, **make_result(status=APIStatus.UnLogin, msg='用户已下线，请重新登陆'))


def get_name_by_session():
    return session["login"]["name"]


def get_user_id_by_session():
    return session["login"]["id"]


def get_user_role_by_session():
    return session["login"]["role"]


def get_payload():
    payload = request.get_json()
    if payload:
        return payload_escape(payload)
    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='缺少请求数据'))


def get_payload_or_400(key):
    value = get_payload().get(key)
    if value is not None:
        return value
    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='payload 缺少请求参数 %s' % (key, )))


def get_arg_or_400(key):
    value = request.args.get(key)
    if value is not None:
        return value
    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='arg 缺少请求参数 %s' % (key, )))


def get_arg_int(key):
    value = request.args.get(key, None)
    if str(value).isdigit():
        return int(value)
    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数 %s 不是 int' % (key,)))


def get_payload_int(key):
    value = get_payload().get(key)
    if str(value).isdigit():
        return int(value)
    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数 %s 不是 int' % (key,)))


def get_arg(key, default=None):
    return request.args.get(key, default)


def get_none_if_empty_arg(key):
    if request.args.get(key, None):
        return request.args.get(key)
    else:
        return None


def get_all_arg():
    # request.args ImmutableMultiDict 是不可变的
    return request.args.to_dict()


def get_device_type():
    # 返回的是什么操作系统类型
    os_header = str(request.headers.get('os', '')).lower()

    if os_header and 'android' in os_header:
        return 1
    elif os_header and 'miniprogram' in os_header:
        return 8
    elif os_header:
        return 2
    else:
        return 4


def get_device_id():
    return request.headers.get('deviceId', '')


def get_version() -> tuple([int, int, int]):
    version = request.headers.get('appVersion')
    if version:
        return tuple(map(int, version.split('.')))
    else:
        return 0, 0, 0
