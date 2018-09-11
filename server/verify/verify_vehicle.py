import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.meta.session_operation import SessionOperationClass
from server.status import HTTPStatus, make_result, APIStatus
from server.utils.extend import Check, compare_time, complement_time


class VerifyVehicle(object):

    @staticmethod
    @make_decorator
    def check_params(page, limit, params):
        try:
            params['mobile'] = int(params.get('mobile') or 0)
            params['vehicle_number'] = str(params.get('vehicle_number') or '')
            params['home_station_id'] = int(params.get('home_station_id') or 0)
            params['vehicle_length'] = str(params.get('vehicle_length') or '')
            params['verify_start_time'] = int(params.get('verify_start_time') or 0)
            params['verify_end_time'] = int(params.get('verify_end_time') or 0)
            params['last_login_start_time'] = int(params.get('last_login_start_time') or 0)
            params['last_login_end_time'] = int(params.get('last_login_end_time') or 0)

            params['verify_start_time'], params['verify_end_time'] = complement_time(params['verify_start_time'], params['verify_end_time'])
            params['last_login_start_time'], params['last_login_end_time'] = complement_time(params['last_login_start_time'], params['last_login_end_time'])

            # 校验手机号码
            if params.get('mobile'):
                if not Check.is_mobile(params['mobile']):
                    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='手机号非法'))

            # 校验是否登录和权限
            if SessionOperationClass.check():
                role, locations_id = SessionOperationClass.get_locations()
                if ('区镇合伙人' in role or '网点管理员' in role or '城市经理' in role) and not params.get('region_id'):
                    params['region_id'] = locations_id
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请登录'))

            # 校验时间参数
            if not compare_time(params['verify_start_time'], params['verify_end_time']):
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求认证时间参数有误'))

            if not compare_time(params['last_login_start_time'], params['last_login_end_time']):
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求最后登录时间参数有误'))

            return Response(page=page, limit=limit, params=params)

        except Exception as e:
            log.error('error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数非法'))
