# coding=utf-8
# author=qiao
from flask import make_response, jsonify

from server import log
from server.status import UserAPIStatus, to_http_status


def direct_response(data: dict):
    assert isinstance(data, dict) and str(data.get('status')).isdigit()
    return make_response(jsonify(data), to_http_status(data['status']))


class MessageException(Exception):
    def __init__(self, message):
        self.message = message


def message_handler(e, *args, func_name=None, **kwargs):
    if isinstance(e, MessageException):
        return make_response(jsonify(e.message), to_http_status(e.message['status']))
    else:
        log.error('%s 运行错误 %s' % (func_name, e), exc_info=True)
        return make_response(jsonify(ServerError), to_http_status(ServerError['status']))


class Error(MessageException):
    def __init__(self, msg):
        self.message = {"msg": msg, "status": UserAPIStatus.BadRequest}


def message_empty_handler(e, *args, **kwargs):
    # if isinstance(e, MessageException):
    #     return make_response(jsonify(e.message), to_http_status(e.message['status']))
    # else:
    log.error('运行错误 %s' % e, exc_info=True)
    return make_response(jsonify({'status': UserAPIStatus.Ok, 'msg': '成功', 'data': {}}), to_http_status(UserAPIStatus.Ok))


NotUser = {"msg": "用户不存在", "status": UserAPIStatus.BadRequest}
PasswordError = {"msg": "密码错误", "status": UserAPIStatus.BadRequest}
MsmCodeError = {"msg": "短信验证码错误", "status": UserAPIStatus.BadRequest}
MsmCodeNotExpire = {"msg": "还未过60秒！不能发送验证码", "status": UserAPIStatus.BadRequest}
GetMsmCodeError = {"msg": "验证码不存在或者已失效，请重新获取", "status": UserAPIStatus.BadRequest}
GetMsmCodeLimit = {"msg": "您的请求过于频繁，请稍后重试！", "status": UserAPIStatus.BadRequest}
SendMsmCodeError = {"msg": "发送验证码失败", "status": UserAPIStatus.BadRequest}
TokenCreateError = {"msg": "TOKEN生成失败", "status": UserAPIStatus.InternalServerError}
DriverIDError = {"msg": "你没有设备ID不允许登录", "status": UserAPIStatus.BadRequest}
UserFreeze = {"msg": "此用户已经被禁用", "status": UserAPIStatus.BadRequest}
UserExist = {"msg": "此用户已存在", "status": UserAPIStatus.BadRequest}
UserError = {"msg": "用户认证异常", "status": UserAPIStatus.BadRequest}
NoLogin = {"msg": "你没有登陆信息", "status": UserAPIStatus.BadRequest}
DriverFreeze = {"msg": "此设备已经被禁用", "status": UserAPIStatus.BadRequest}

ServerError = {"msg": "服务器异常", "status": UserAPIStatus.InternalServerError}
