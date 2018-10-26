# -*- coding: utf-8 -*-
from flask_restful import abort

from server import log
from server.database import db
from server.models.fresh import FreshModel
from server.models.goods import GoodsList, CancelReasonList, GoodsDistributionTrendList
from server.status import make_resp, APIStatus, HTTPStatus


def get_goods_list(params):
    if params.get('new_goods_type') == 1:
        user_id_list = FreshModel.get_fresh_consignor_id(db.read_db, params.get('node_id'))
    else:
        user_id_list = None

    goods_list = GoodsList.get_goods_list(db.read_db, user_id_list, params)

    return goods_list


def get_goods_cancel_reason_list(params):
    try:
        cancel_reason_list = CancelReasonList.get_cancel_reason_list(db.read_db, params)
        return make_resp(APIStatus.Ok, data=cancel_reason_list), HTTPStatus.Ok
    except Exception as e:
        log.error('查询货源取消原因出现错误 [Error: %s]' % e)
        abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='查询货源取消原因出现错误'))


def get_goods_distribution_trend(params):
    try:
        goods_distribution_trend = GoodsDistributionTrendList.get_goods_distribution_trend(db.read_db, params)
        return goods_distribution_trend
    except Exception as e:
        log.error('查询货源趋势出现错误 [Error: %s]' % e)
        abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='查询货源趋势出现错误'))



