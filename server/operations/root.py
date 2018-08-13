from flask_restful import abort

from server import log
from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.root import RootManagementModel
from server.status import HTTPStatus, make_result, APIStatus


class RootManagement(object):

    @staticmethod
    @make_decorator
    def get_data(params):
        data = RootManagementModel.get_data(db.read_bi, params)

        return Response(data=data)

    @staticmethod
    @make_decorator
    def put_data(params):
        try:
            rowcount = RootManagementModel.put_data(db.write_bi, params)
            if rowcount:
                return make_result(APIStatus.Ok), HTTPStatus.Ok
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.InternalServerError, msg='修改账户信息失败'))
        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='修改账户信息失败'))


    @staticmethod
    @make_decorator
    def delete_data(params):
        try:
            rowcount = RootManagementModel.delete_data(db.write_bi, params)
            if rowcount:
                return make_result(APIStatus.Ok), HTTPStatus.Ok
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.InternalServerError, msg='账户不存在，删除账户失败'))
        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.InternalServerError, msg='删除账户失败'))


    @staticmethod
    @make_decorator
    def post_data(params):
        try:
            user_id = RootManagementModel.post_data(db.write_bi, params)
            if user_id:
                return make_result(APIStatus.Ok), HTTPStatus.Ok
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.InternalServerError, msg='添加账户失败'))

        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.InternalServerError, msg='添加账户失败'))

