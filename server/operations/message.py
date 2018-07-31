from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.message import MessageWindowModel


class MessageWindow(object):

    @staticmethod
    @make_decorator
    def get_message(params):
        data = MessageWindowModel.get_data(db.read_db, params)
        return Response(data=data)
