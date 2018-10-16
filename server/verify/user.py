# -*- coding: utf-8 -*-

import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.meta.session_operation import SessionOperationClass
from server.status import HTTPStatus, make_resp, APIStatus
from server.utils.extend import compare_time, complement_time
from server.utils.role_regions import get_role_regions


class UserStatistic(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            if not SessionOperationClass.check():
                abort(HTTPStatus.Forbidden, **make_resp(status=APIStatus.UnLogin, msg='未登录'))

            params['start_time'] = int(params.get('start_time') or time.time() - 86400 * 7)
            params['end_time'] = int(params.get('end_time') or time.time() - 86400)
            params['periods'] = int(params.get('periods') or 2)
            params['user_type'] = int(params.get('user_type') or 1)
            params['role_type'] = int(params.get('role_type') or 0)
            params['region_id'] = int(params.get('region_id') or 0)
            params['is_auth'] = int(params.get('is_auth') or 0)

            # 补全时间
            params['start_time'], params['end_time'] = complement_time(params['start_time'], params['end_time'])
            # 校验时间
            if not compare_time(params['start_time'], params['end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='时间参数有误'))
            # 获取权限地区id
            params['region_id'] = get_role_regions(params['region_id'])

            return Response(params=params)
        except Exception as e:
            log.warn('请求参数非法:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='请求参数非法'))

    @staticmethod
    @make_decorator
    def check_behavior_params(params):
        try:
            if not SessionOperationClass.check():
                abort(HTTPStatus.Forbidden, **make_resp(status=APIStatus.UnLogin, msg='未登录'))
            params['start_time'] = int(params.get('start_time') or time.time() - 86400 * 7)
            params['end_time'] = int(params.get('end_time') or time.time())
            params['periods'] = int(params.get('periods') or 2)
            params['data_type'] = int(params.get('data_type') or 1)

            # 补全时间
            params['start_time'], params['end_time'] = complement_time(params['start_time'], params['end_time'])
            # 校验时间
            if not compare_time(params['start_time'], params['end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='时间参数有误'))
            # 获取权限地区id
            params['region_id'] = get_role_regions(0)

            return Response(params=params)
        except Exception as e:
            log.error('请求参数非法:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='请求参数非法'))


class UserList(object):

    @staticmethod
    @make_decorator
    def check_params(page, limit, params):
        try:
            if not SessionOperationClass.check():
                abort(HTTPStatus.Forbidden, **make_resp(status=APIStatus.UnLogin, msg='未登录'))

            params['user_name'] = str(params.get('user_name') or '')
            params['mobile'] = int(params.get('mobile') or 0)
            params['reference_mobile'] = int(params.get('reference_mobile') or 0)
            params['download_ch'] = str(params.get('download_ch') or '')
            params['from_channel'] = str(params.get('from_channel') or '')
            params['is_referenced'] = int(params.get('is_referenced') or 0)
            params['region_id'] = int(params.get('region_id') or 0)
            params['role_type'] = int(params.get('role_type') or 0)
            params['role_auth'] = int(params.get('role_auth') or 0)
            params['is_actived'] = int(params.get('is_actived') or 0)
            params['is_used'] = int(params.get('is_used') or 0)
            params['is_car_sticker'] = int(params.get('is_car_sticker') or 0)
            params['last_login_start_time'] = int(params.get('last_login_start_time') or 0)
            params['last_login_end_time'] = int(params.get('last_login_end_time') or 0)
            params['register_start_time'] = int(params.get('register_start_time') or 0)
            params['register_end_time'] = int(params.get('register_end_time') or 0)

            params['last_login_start_time'], params['last_login_end_time'] = complement_time(params['last_login_start_time'], params['last_login_end_time'])
            params['register_start_time'], params['register_end_time'] = complement_time(params['register_start_time'], params['register_end_time'])

            # 检验最后登陆时间
            if not compare_time(params['last_login_start_time'], params['last_login_end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='最后登录时间有误'))

            # 检验注册时间
            if not compare_time(params['register_start_time'], params['register_end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='注册时间有误'))

            # 获取权限地区id
            params['region_id'] = get_role_regions(params['region_id'])

            log.debug("用户列表验证参数{}".format(params))

            return Response(page=page, limit=limit, params=params)

        except Exception as e:
            log.warn("用户列表验证参数错误{}".format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='请求参数有误'))
