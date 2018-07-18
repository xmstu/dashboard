from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.verify_vehicle import VerifyVehicleModel


class VerifyVehicle(object):

    @staticmethod
    @make_decorator
    def get_list(params):
        data = VerifyVehicleModel.get_data(db.read_db, params)

        return Response(data=data)