import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.status import HTTPStatus, make_resp, APIStatus
from server.utils.extend import Check, compare_time, complement_time
from server.meta.session_operation import SessionOperationClass


class PromoteEffect(object):

    @staticmethod
    @make_decorator
    def check_params(page, limit, params):

        try:
            if not SessionOperationClass.check():
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.UnLogin, msg='请登录'))

            params['user_name'] = str(params.get('user_name') or '')
            params['mobile'] = str(params.get('mobile') or '')
            params['goods_type'] = int(params.get('goods_type') or 0)
            params['register_start_time'] = int(params.get('register_start_time') or 0)
            params['register_end_time'] = int(params.get('register_end_time') or 0)
            params['statistic_start_time'] = int(params.get('statistic_start_time') or 0)
            params['statistic_end_time'] = int(params.get('statistic_end_time') or 0)

            # 补全时间
            params['register_start_time'], params['register_end_time'] = complement_time(params['register_start_time'], params['register_end_time'])
            params['statistic_start_time'], params['statistic_end_time'] = complement_time(params['statistic_end_time'], params['statistic_end_time'])

            # 判断时间是否合法
            if not compare_time(params['register_start_time'], params['register_end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.Forbidden, msg='时间参数有误'))

            if not compare_time(params['statistic_start_time'], params['statistic_end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.Forbidden, msg='时间参数有误'))

            if params['mobile']:
                if not Check.is_mobile(params['mobile']):
                    abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.Forbidden, msg='手机号非法'))

            # 获取用户权限和身份
            role_big_type, user_id = SessionOperationClass.get_role()
            regions = SessionOperationClass.get_user_locations()

            params['role_big_type'] = role_big_type
            params['regions'] = regions
            params['user_id'] = user_id

            return Response(page=page, limit=limit, params=params)

        except Exception as e:
            log.error('Error:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.Forbidden, msg='参数有误'))
            
    @staticmethod
    @make_decorator
    def check_add_params(role_type, user_id, payload):
        mobile = payload.get('mobile', '')
        user_name = payload.get('user_name', '')
        if not role_type == 4:
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='非城市经理不能添加推广人员'))
        if not user_id:
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='管理员id不存在'))
        if not Check.is_mobile(mobile):
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='手机号非法'))
        if not user_name:
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='推广人姓名不能为空'))
        return Response(user_id=user_id, mobile=mobile, user_name=user_name)

    @staticmethod
    @make_decorator
    def check_delete_params(role_type, user_id, promoter_mobile):
        if not role_type == 4:
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='非城市经理不能删除推广人员'))
        if not user_id:
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='管理员id不存在'))
        if not promoter_mobile:
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='推广人员不存在'))
        return Response(user_id=user_id, promoter_mobile=promoter_mobile)


class PromoteQuality(object):

    @staticmethod
    @make_decorator
    def check_params(params):

        try:
            if not SessionOperationClass.check():
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.UnLogin, msg='请登录'))
            # 校验参数
            params['start_time'] = int(params.get('start_time')) if params.get('start_time') else time.time() - 86400*7
            params['end_time'] = int(params.get('end_time')) if params.get('end_time') else time.time() - 86400
            params['periods'] = int(params.get('periods')) if params.get('periods') else 2
            params['dimension'] = int(params.get('dimension')) if params.get('dimension') else 1
            params['data_type'] = int(params.get('data_type')) if params.get('data_type') else 1

            # 获取用户权限和身份
            role_type, user_id = SessionOperationClass.get_role()
            regions = SessionOperationClass.get_user_locations()

            if not compare_time(params['start_time'], params['end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='时间参数非法'))

            params['role_type'] = role_type
            params['user_id'] = user_id
            params['regions'] = regions

            return Response(params=params)
        except Exception as e:
            log.warn('Error:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.Forbidden, msg='请求参数非法'))
