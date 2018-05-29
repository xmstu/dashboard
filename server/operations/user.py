# -*- coding: utf-8 -*-
from flask_restful import abort

from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.user import UserList
from server.status import HTTPStatus, make_result, APIStatus


class UserListDecorator(object):

    @staticmethod
    @make_decorator
    def get_user_list(params):
        user_list = UserList.get_user_list(db.read_io, params)
        if not user_list:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='找不到用户列表'))
        return Response(user_list=user_list)
