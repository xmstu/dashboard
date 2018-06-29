import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.status import HTTPStatus, make_result, APIStatus
from server.utils.extend import Check
from server.meta.session_operation import sessionOperationClass

class PromoteEffect(object):

    @staticmethod
    @make_decorator
    def check_params(page, limit, params):

        try:
            # 通过params获取参数，获取不到就赋予默认值
            user_name = params.get('user_name', '')
            mobile = params.get('mobile', '')
            role_type = int(params.get('role_type')) if params.get('role_type') else 0
            goods_type = int(params.get('goods_type')) if params.get('goods_type') else 0
            is_actived = int(params.get('is_actived')) if params.get('is_actived') else 0
            is_car_sticker = int(params.get('is_car_sticker')) if params.get('is_car_sticker') else 0
            start_time = int(params.get('start_time')) if params.get('start_time') else 0
            end_time = int(params.get('end_time')) if params.get('end_time') else 0

            # 获取用户权限和身份
            role, user_id = sessionOperationClass.get_role()

            # 判断时间是否合法
            if start_time and end_time:
                if start_time <= end_time:
                    pass
                else:
                    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间参数有误'))
            elif not start_time and not end_time:
                pass
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间参数有误'))

            # 构造请求参数
            params = {
                'role': role,
                'user_id': user_id,
                'user_name': user_name,
                'mobile': mobile,
                'role_type': role_type,
                'goods_type': goods_type,
                'is_actived': is_actived,
                'is_car_sticker': is_car_sticker,
                'start_time': start_time,
                'end_time': end_time
            }

            return Response(page=page, limit=limit, params=params)

        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数有误'))
            
    @staticmethod
    @make_decorator
    def check_add_params(role, user_id, payload):
        mobile = payload.get('mobile', '')
        user_name = payload.get('user_name', '')
        if role != 4:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='非城市经理不能添加推广人员'))
        if not user_id:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='管理员id不存在'))
        if not Check.is_mobile(mobile):
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='手机号非法'))
        if not user_name:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='推广人姓名不能为空'))
        return Response(user_id=user_id, mobile=mobile, user_name=user_name)


    @staticmethod
    @make_decorator
    def check_delete_params(role, user_id, promoter_id):
        if role != 4:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='非城市经理不能删除推广人员'))
        if not user_id:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='管理员id不存在'))
        if not promoter_id:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='推广人员不存在'))
        return Response(user_id=user_id, promoter_id=promoter_id)

class PromoteQuality(object):

    @staticmethod
    @make_decorator
    def check_params(params):

        try:
            # 校验参数
            start_time = int(params.get('start_time')) if params.get('start_time') else time.time() - 8 * 60 * 60 * 24
            end_time = int(params.get('end_time')) if params.get('end_time') else time.time() - 60 * 60 * 24
            periods = int(params.get('periods')) if params.get('periods') else 2
            dimension = int(params.get('dimension')) if params.get('dimension') else 1
            data_type = int(params.get('data_type')) if params.get('data_type') else 1

            # 获取用户权限和身份
            role, user_id = sessionOperationClass.get_role()

            # 验证参数
            if start_time and end_time:
                if start_time <= end_time:
                    pass
                else:
                    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间参数有误'))
            elif not start_time and not end_time:
                pass
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间参数有误'))

            params = {
                'start_time': start_time,
                'end_time': end_time,
                'periods': periods,
                'dimension': dimension,
                'data_type': data_type,
                'role': role,
                'user_id': user_id
            }

            return Response(params=params)
        except Exception as e:
            log.warn('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求参数非法'))
