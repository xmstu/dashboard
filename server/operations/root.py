from flask_restful import abort

from server import log
from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.root import RootManagementModel, RootRoleManagementModel, RootPageManagementModel
from server.status import HTTPStatus, make_result, APIStatus


class RootManagement(object):

    @staticmethod
    @make_decorator
    def get_data(params):
        data = RootManagementModel.get_data(db.read_bi, params)

        return Response(data=data)

    @staticmethod
    @make_decorator
    def get_role(admin_id):
        data = RootManagementModel.get_role(db.read_bi, admin_id)

        return make_result(APIStatus.Ok, data=data), HTTPStatus.Ok

    @staticmethod
    @make_decorator
    def put_data(params):
        try:
            rowcount = RootManagementModel.put_data(db.write_bi, params)
            if rowcount:
                return make_result(APIStatus.Ok), HTTPStatus.Ok
            else:
                abort(HTTPStatus.InternalServerError, **make_result(status=APIStatus.InternalServerError, msg='修改账户信息失败'))
        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_result(status=APIStatus.InternalServerError, msg='修改账户信息失败'))

    @staticmethod
    @make_decorator
    def delete_data(params):
        try:
            rowcount = RootManagementModel.delete_data(db.write_bi, params)
            if rowcount:
                return make_result(APIStatus.Ok), HTTPStatus.Ok
            else:
                abort(HTTPStatus.InternalServerError, **make_result(status=APIStatus.InternalServerError, msg='账户不存在，删除账户失败'))
        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_result(status=APIStatus.InternalServerError, msg='删除账户失败'))


    @staticmethod
    @make_decorator
    def post_data(params):
        try:
            admin_id = RootManagementModel.post_data(db.write_bi, params)
            if admin_id:
                return make_result(APIStatus.Ok), HTTPStatus.Ok
            else:
                abort(HTTPStatus.InternalServerError, **make_result(status=APIStatus.InternalServerError, msg='添加账户失败'))

        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_result(status=APIStatus.InternalServerError, msg='添加账户失败'))


class RootRoleManagement(object):

    @staticmethod
    @make_decorator
    def get_role_list(params):
        data = RootRoleManagementModel.get_role_list(db.read_bi, params)
        return Response(data=data)

    @staticmethod
    @make_decorator
    def post_data(params):
        try:
            role_id = RootRoleManagementModel.post_data(db.write_bi, params)
            if role_id:
                return make_result(APIStatus.Ok), HTTPStatus.Ok
            else:
                abort(HTTPStatus.InternalServerError, **make_result(status=APIStatus.InternalServerError, msg='添加角色失败'))
        except Exception as e:
            log.error('添加角色失败,失败原因是:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_result(status=APIStatus.InternalServerError, msg='添加角色失败'))

    @staticmethod
    @make_decorator
    def put_data(params):
        try:
            rowcount = RootRoleManagementModel.put_data(db.write_bi, params)
            if rowcount:
                return make_result(APIStatus.Ok), HTTPStatus.Ok
            else:
                abort(HTTPStatus.InternalServerError, **make_result(status=APIStatus.InternalServerError, msg='修改角色失败'))
        except Exception as e:
            log.error('修改角色失败,失败原因是:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_result(status=APIStatus.InternalServerError, msg='修改角色失败'))

    @staticmethod
    @make_decorator
    def delete_data(params):
        try:
            rowcount = RootRoleManagementModel.delete_data(db.write_bi, params)
            if rowcount:
                return make_result(APIStatus.Ok), HTTPStatus.Ok
            else:
                abort(HTTPStatus.InternalServerError,
                      **make_result(status=APIStatus.InternalServerError, msg='账户不存在，删除账户失败或账户不能重复删除'))
        except Exception as e:
            log.error('删除角色失败,失败原因是:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_result(status=APIStatus.InternalServerError, msg='删除角色失败'))

    @staticmethod
    @make_decorator
    def get_role_pages(params):
        try:
            page_list = RootRoleManagementModel.get_role_pages(db.read_bi, params)
            return make_result(status=APIStatus.Ok, data=page_list), HTTPStatus.Ok
        except Exception as e:
            log.error('获取当前角色的权限页面失败:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_result(status=APIStatus.InternalServerError, msg='获取当前角色的权限页面失败'))


class RootPageManagement(object):

    @staticmethod
    @make_decorator
    def get_all_pages(params):
        try:
            data = RootPageManagementModel.get_all_pages(db.read_bi, params)
            return make_result(status=APIStatus.Ok, data=data), HTTPStatus.Ok
        except Exception as e:
            log.error('获取所有页面失败:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_result(status=APIStatus.InternalServerError, msg='获取所有页面失败'))

    @staticmethod
    @make_decorator
    def post_data(params):
        try:
            page_id = RootPageManagementModel.post_data(db.write_bi, params)
            if page_id:
                return make_result(APIStatus.Ok), HTTPStatus.Ok
            else:
                abort(HTTPStatus.InternalServerError, **make_result(status=APIStatus.InternalServerError, msg='添加页面失败'))
        except Exception as e:
            log.error('添加页面失败:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_result(status=APIStatus.InternalServerError, msg='添加页面失败'))
