from flask_restful import abort

from server import log
from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.active_retain import ActiveUserStatisticModel
from server.status import HTTPStatus, make_resp, APIStatus


class ActiveUserStatistic(object):

    @staticmethod
    @make_decorator
    def get_active_user_statistic(params):
        try:
            data = ActiveUserStatisticModel.get_active_user_statistic(db.read_db, db.read_bi, params)
            return Response(params=params, data=data)
        except Exception as e:
            log.error('查询活跃用户趋势出现错误 [Error: %s]' % e)
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='查询活跃用户趋势出现错误'))

