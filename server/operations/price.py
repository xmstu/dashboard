from flask_restful import abort

from server import log
from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.price import PriceTrendModel
from server.status import HTTPStatus, make_result, APIStatus


class PriceTrend(object):

    @staticmethod
    @make_decorator
    def get_data(params):
        try:
            data = PriceTrendModel.get_data(db.read_db, params)
            return Response(data=data)
        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求参数有误'))
