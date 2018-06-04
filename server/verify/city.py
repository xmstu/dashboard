from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.status import HTTPStatus, make_result, APIStatus


class CityOrderList(object):

    @staticmethod
    @make_decorator
    def check_params(page, limit, params):
        # 通过params获取参数
        try:

            goods_type = int(params.get('goods_type')) if params.get('goods_type') else 0
            priority = int(params.get('priority')) if params.get('priority') else 0
            vehicle_length = int(params.get('vehicle_length')) if params.get('vehicle_length') else 0
            is_called = int(params.get('is_called')) if params.get('is_called') else 0
            is_addition = int(params.get('is_addition')) if params.get('is_addition') else 0
            node_id = int(params.get('node_id')) if params.get('node_id') else 0
            new_goods_type = int(params.get('new_goods_type')) if params.get('new_goods_type') else 0

            # TODO 校验参数

            params = {

                "goods_type": goods_type,
                "priority": priority,
                "is_called": is_called,
                "vehicle_length": vehicle_length,
                "node_id": node_id,
                "new_goods_type": new_goods_type,
                "is_addition": is_addition,
            }
            log.info("params:{}".format(params))
            return Response(page=page, limit=limit, params=params)

        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求参数有误'))
