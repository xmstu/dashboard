import hashlib

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.status import HTTPStatus, make_result, APIStatus
from server.utils.extend import pwd_to_hash, Check


class RootManagement(object):

    @staticmethod
    @make_decorator
    def check_get_params(params):
        try:
            if not params.get('page') or not params['page'].isdigit():
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='页数错误'))
            if not params.get('limit') or not params['limit'].isdigit():
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='条数错误'))
            params['page'], params['limit'] = (int(params['page']) - 1) * int(params['limit']), int(params['limit'])
            return Response(params=params)
        except Exception as e:
            log.error('error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数非法'))

    @staticmethod
    @make_decorator
    def check_put_params(params):
        try:
            params['account'] = str(params.get('account') or '')
            params['user_name'] = str(params.get('user_name') or '')
            pwd = str(params.get('password') or '')
            params['role_id'] = int(params.get('role_id') or 0)
            params['admin_id'] = int(params.get('admin_id') or 0)
            params['is_active'] = int(params.get('is_active') or 0)
            # 加密密码
            if pwd:
                params['password'] = pwd_to_hash(pwd)
            return Response(params=params)
        except Exception as e:
            log.error('error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数非法'))

    @staticmethod
    @make_decorator
    def check_post_params(params):
        try:
            params['account'] = str(params.get('account') or '')
            params['user_name'] = str(params.get('user_name') or '')
            params['password'] = pwd = str(params.get('password') or '')
            params['role_id'] = int(params.get('role_id') or 0)
            params['is_active'] = int(params.get('is_active') or 0)

            if not Check.is_mobile(params['account']):
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='账号非法'))
            # 加密密码
            params['password'] = pwd_to_hash(pwd)

            return Response(params=params)
        except Exception as e:
            log.error('error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数非法'))


class RootRoleManagement(object):

    @staticmethod
    @make_decorator
    def check_post_params(params):
        try:
            params['role_name'] = str(params.get('role_name') or '')
            params['role_comment'] = str(params.get('role_comment') or '')
            params['region_id'] = int(params.get('region_id') or 0)
            params['page_id_list'] = str(params.get('page_id_list') or '')

            # 参数校验
            if not params['role_name']:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='必须要有角色名称'))

            if not params['region_id']:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='最起码要有一个地区id'))

            if not params['page_id_list']:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='最起码要有一个页面id'))

            params['page_id_list'] = [int(i) for i in params['page_id_list'].split(',')]

            return Response(params=params)
        except Exception as e:
            log.error('校验新增角色参数时出错,错误是:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数非法'))

    @staticmethod
    @make_decorator
    def check_put_params(params):
        try:
            params['role_id'] = int(params.get('role_id') or 0)

            params['role_name'] = str(params.get('role_name') or '')
            params['role_comment'] = str(params.get('role_comment') or '')
            params['region_id'] = int(params.get('region_id') or 0)
            params['page_id_list'] = str(params.get('page_id_list') or '')

            # 判断role_id是否存在
            if not params['role_id']:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='role_id不能为空或0'))

            # 参数校验
            if not params['role_name'] and not params['role_comment'] and not params['region_id'] and not params['page_id_list']:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='最起码请输入一个参数'))

            # 如果有page_id_list
            if params['page_id_list']:
                params['page_id_list'] = [int(i) for i in params['page_id_list'].split(',')]

            return Response(params=params)
        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求参数有误'))


class RootPageManagement(object):

    @staticmethod
    @make_decorator
    def post_data(params):
        try:
            params['page_name'] = str(params.get('page_name') or '')
            params['page_comment'] = str(params.get('page_comment') or '')
            params['page_path'] = str(params.get('page_path') or '')
            params['parent_menu_id'] = int(params.get('parent_menu_id') or 0)

            # 判断是否传入页面名称
            if not params['page_name']:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请传入页面名称'))
            # 判断是否传入页面路径
            if not params['page_path']:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请传入路径'))
            # 判断是否有父菜单id
            if not params['parent_menu_id']:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请传入父菜单id'))
            return Response(params=params)
        except Exception as e:
            log.error('请求参数有误:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求参数有误'))

    @staticmethod
    @make_decorator
    def put_data(params):
        try:
            params['page_name'] = str(params.get('page_name') or '')
            params['page_comment'] = str(params.get('page_comment') or '')
            params['page_path'] = str(params.get('page_path') or '')
            params['parent_menu_id'] = int(params.get('parent_menu_id') or 0)

            if not params['page_name'] and not params['page_comment'] and not params['page_path'] and not params['parent_menu_id']:
                    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='最起码请传一个参数'))

            return Response(params=params)
        except Exception as e:
            log.error('请求参数有误:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求参数有误'))
