# -*- coding: utf-8 -*-
from flask_restful import abort

from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.promote import PromoteEffetList
from server.status import HTTPStatus, make_result, APIStatus


class PromoteEffectDecorator(object):

    @staticmethod
    @make_decorator
    def get_promote_effet_list(page, limit, params):
        promote_effet_list = PromoteEffetList.get_promote_effet_list(db.read_db, page, limit, params)

        return Response(promote_effet_list=promote_effet_list)
