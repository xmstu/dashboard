# -*- coding: utf-8 -*-

from flask_restful import abort
import time

from server.meta.decorators import make_decorator, Response
from server.status import HTTPStatus, make_resp, APIStatus
from server import log


class CityManagerVerify(object):
    @staticmethod
    @make_decorator
    def check_params(params):
        """城市经理提成接口参数验证"""
        if not params.get('mobile'):
            abort(HTTPStatus.BadRequest, **make_resp(HTTPStatus.BadRequest, msg='用户名不存在'))
        if not params.get('start_time'):
            abort(HTTPStatus.BadRequest, **make_resp(HTTPStatus.BadRequest, msg='开始时间不存在'))
        if not params.get('end_time'):
            abort(HTTPStatus.BadRequest, **make_resp(HTTPStatus.BadRequest, msg='结束时间不存在'))
        mobile = params.get('mobile')
        try:
            start_time = time.mktime(time.strptime(params.get('start_time') + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
        except:
            abort(HTTPStatus.BadRequest, **make_resp(HTTPStatus.BadRequest, msg='开始时间格式错误'))

        try:
            end_time = time.mktime(time.strptime(params.get('end_time') + ' 23:59:59', '%Y-%m-%d %H:%M:%S'))
        except:
            abort(HTTPStatus.BadRequest, **make_resp(HTTPStatus.BadRequest, msg='结束时间格式错误'))

        result = {
            "mobile": mobile,
            "start_time": int(start_time),
            "end_time": int(end_time)
        }
        return Response(params=result)