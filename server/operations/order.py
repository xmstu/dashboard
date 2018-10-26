from flask_restful import abort

from server import log
from server.database import db
from server.models.fresh import FreshModel
from server.models.order import OrdersReceivedStatisticsList, CancelOrderReasonModel, OrderListModel
from server.status import HTTPStatus, make_resp, APIStatus


def orders_received_statistics_get_data(params):
    try:
        data = OrdersReceivedStatisticsList.get_order_received_statistics_list(db.read_db, params)
        return data
    except Exception as e:
        log.error('查询订单趋势出现错误 [Error: %s]' % e)
        abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='查询订单趋势出现错误'))


def cancel_order_get_data(params):
    try:
        data = CancelOrderReasonModel.get_cancel_order_reason(db.read_db, params)
        return data
    except Exception as e:
        log.error('查询订单取消原因出现错误 [Error: %s]' % e)
        abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='查询订单取消原因出现错误'))


def order_list_get_data(params):

    try:
        if params.get('spec_tag') == 1:
            fresh_ids = FreshModel.get_fresh_consignor_id(db.read_db, params.get('region_id'))
        elif params.get('spec_tag') == 2:
            fresh_ids = FreshModel.get_fresh_driver_id(db.read_db, params.get('region_id'))
        else:
            fresh_ids = ['0']
        data = OrderListModel.get_order_list(db.read_db, fresh_ids, params)

        return data
    except Exception as e:
        log.error('查询订单列表出现错误 [Error: %s]' % e)
        abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='查询订单列表出现错误'))
