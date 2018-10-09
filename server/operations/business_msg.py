from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.business_msg import BusinessMsgListModel
from server.status import make_resp, APIStatus, HTTPStatus


class BusinessMsgList(object):

    @staticmethod
    @make_decorator
    def get_data(params):
        data = BusinessMsgListModel.get_msg(db.read_db, params)
        if not data:
            return make_resp(APIStatus.Ok, count=0, data=[]), HTTPStatus.Ok
        return Response(data=data)
