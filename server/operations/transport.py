from flask_restful import abort

from server import log
from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.transport import TransportRadarModel, TransportListModel
from server.status import HTTPStatus, make_resp, APIStatus


class TransportRadar(object):

    @staticmethod
    @make_decorator
    def get_trend(params):
        try:
            data = TransportRadarModel.get_data(db.read_bi, params)
            if data:
                return make_resp(status=APIStatus.Ok, data=data), HTTPStatus.Ok
            else:
                abort(HTTPStatus.InternalServerError,
                      **make_resp(status=APIStatus.InternalServerError, msg='获取雷达图数据失败'))
        except Exception as e:
            log.error('获取雷达图数据失败:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='获取雷达图数据失败'))


class TransportList(object):

    @staticmethod
    @make_decorator
    def get_list(params):
        try:
            data = TransportListModel.get_data(db.read_db, params)
            if data:
                return Response(params=params, data=data)
            else:
                abort(HTTPStatus.InternalServerError,
                      **make_resp(status=APIStatus.InternalServerError, msg='获取运力列表数据失败'))
        except Exception as e:
            log.error('获取运力列表数据失败:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='获取运力列表数据失败'))

