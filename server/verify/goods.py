import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.status import HTTPStatus, make_result, APIStatus


class GoodsList(object):

    @staticmethod
    @make_decorator
    def check_params(page, limit, params):
        # 通过params获取参数

        try:
            goods_id = params.get('goods_id') if params.get('goods_id') else ''
            mobile = params.get('mobile') if params.get('mobile') else ''
            from_region_id = params.get('from_region_id') if params.get('from_region_id') else ''
            to_region_id = params.get('to_region_id') if params.get('to_region_id') else ''

            goods_type = int(params.get('goods_type')) if params.get('goods_type') else 0
            goods_status = int(params.get('goods_status')) if params.get('goods_status') else 0
            is_called = int(params.get('is_called')) if params.get('is_called') else 0
            vehicle_length = int(params.get('vehicle_length')) if params.get('vehicle_length') else 0
            vehicle_type = int(params.get('vehicle_type')) if params.get('vehicle_type') else 0
            node_id = int(params.get('node_id')) if params.get('node_id') else 0
            new_goods_type = int(params.get('new_goods_type')) if params.get('new_goods_type') else 0
            urgent_goods = int(params.get('urgent_goods')) if params.get('urgent_goods') else 0
            is_addition = int(params.get('is_addition')) if params.get('is_addition') else 0

            create_start_time = int(params.get('create_start_time')) if params.get('create_start_time') else 0
            create_end_time = int(params.get('create_end_time')) if params.get('create_end_time') else 0
            load_start_time = int(params.get('load_start_time')) if params.get('load_start_time') else 0
            load_end_time = int(params.get('load_end_time')) if params.get('load_end_time') else 0

            # TODO 校验参数
            if create_end_time and create_start_time:
                if (create_start_time < create_end_time) and (create_end_time < time.time()):
                    pass
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='发布时间有误'))

            if load_start_time and load_end_time:
                if (load_start_time < load_end_time) and (load_end_time < time.time()):
                    pass
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='装货时间有误'))

            params = {
                "goods_id": goods_id,
                "mobile": mobile,
                "from_region_id": from_region_id,
                "to_region_id": to_region_id,
                "goods_type": goods_type,
                "goods_status": goods_status,
                "is_called": is_called,
                "vehicle_length": vehicle_length,
                "vehicle_type": vehicle_type,
                "node_id": node_id,
                "new_goods_type": new_goods_type,
                "urgent_goods": urgent_goods,
                "is_addition": is_addition,
                "create_start_time": create_start_time,
                "create_end_time": create_end_time,
                "load_start_time": load_start_time,
                "load_end_time": load_end_time,
            }
            log.info("params:{}".format(params))
            return Response(page=page, limit=limit, params=params)

        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求参数有误'))
