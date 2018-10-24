from flask_restful import abort

from server import log
from server.database import db
from server.models.verify_vehicle import VerifyVehicleModel
from server.status import HTTPStatus, make_resp, APIStatus


def verify_vehicle_get_list(params):
    try:
        data = VerifyVehicleModel.get_data(db.read_db, params)
        return data
    except Exception as e:
        log.error('查询认证车辆出现错误 [Error: %s]' % e)
        abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='查询认证车辆出现错误'))
