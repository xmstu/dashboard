# -*- coding: utf-8 -*-
from flask_restful import abort

from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.goods import GoodsList
from server.status import HTTPStatus, make_result, APIStatus


class GoodsListDecorator(object):

    @staticmethod
    @make_decorator
    def get_goods_list(page, limit, params):
        goods_list = GoodsList.get_goods_list(db.read_io, page, limit, params)

        if not goods_list:
            abort(HTTPStatus.NotFound, **make_result(status=APIStatus.NotFound, msg='找不到货源列表'))

        return Response(data=goods_list)
