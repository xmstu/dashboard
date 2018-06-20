import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.status import HTTPStatus, make_result, APIStatus


class OrdersReceivedStatistics(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            params['start_time'] = int(params.get('start_time', None) or time.time() - 86400 * 8)
            params['end_time'] = int(params.get('end_time', None) or time.time() - 86400)
            params['periods'] = int(params.get('periods', None) or 2)
            params['goods_type'] = int(params.get('goods_type', None) or 0)
            params['dimension'] = int(params.get('dimension', None) or 1)
            params['region_id'] = int(params.get('region_id', None) or 0)
            params['comment_type'] = int(params.get('comment_type', None) or 0)
            params['pay_method'] = int(params.get('pay_method', None) or 0)

            if params['start_time'] <= params['end_time'] < time.time():
                pass
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求时间参数有误'))

            return Response(params=params)
        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求参数有误'))


class CancelOrderReason(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            params['start_time'] = int(params.get('start_time', None) or time.time() - 86400 * 7)
            params['end_time'] = int(params.get('end_time', None) or time.time() - 86400)
            params['goods_type'] = int(params.get('goods_type', None) or 0)
            params['cancel_type'] = int(params.get('cancel_type',None) or 1)
            params['region_id'] = int(params.get('region_id', None) or 0)

            if params['start_time'] <= params['end_time'] < time.time():
                pass
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求时间参数有误'))

            return Response(params=params)
        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求参数有误'))


class OrderList(object):

    @staticmethod
    @make_decorator
    def check_params(params, **kwargs):
        try:
            pass
        except Exception as e:
            log.error('error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数非法'))