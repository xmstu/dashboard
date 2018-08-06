from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.root import RootManagementModel


class RootManagement(object):

    @staticmethod
    @make_decorator
    def get_data(params):
        data = RootManagementModel.get_data(db.read_bi, params)

        return Response(data=data)

    @staticmethod
    @make_decorator
    def put_data(params):
        data = RootManagementModel.put_data(db.read_bi, params)

        return Response(data=data)

    @staticmethod
    @make_decorator
    def delete_data(params):
        data = RootManagementModel.delete_data(db.read_bi, params)

        return Response(data=data)

    @staticmethod
    @make_decorator
    def add_data(params):
        data = RootManagementModel.delete_data(db.read_bi, params)

        return Response(data=data)
