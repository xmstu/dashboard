from flask_restful import abort

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

    @staticmethod
    @make_decorator
    def put_msg(params):
        if not BusinessMsgListModel.put_msg(db.write_db, params):
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='修改信息得跟进人和跟进结果失败,请检查是否有新的更新信息'))
        return make_resp(APIStatus.Ok, msg="修改信息的跟进人或处理结果成功"), HTTPStatus.Ok

