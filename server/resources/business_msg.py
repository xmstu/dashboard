from flask_restful import abort
from flask_restplus import Resource

from server import api
import server.document.business_msg as doc
from server import operations, filters
from server.meta.decorators import Response
from server.meta.session_operation import SessionOperationClass
from server.status import HTTPStatus, make_resp, APIStatus
from server.utils.request import get_all_arg, get_payload


class BusinessMsg(Resource):

    @doc.request_business_msg_list_get
    @filters.BusinessMsgList.get_result(data=dict)
    @operations.BusinessMsgList.get_data(params=dict)
    def get(self):
        params = get_all_arg()
        if not params.get('page') or not params['page'].isdigit():
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='页数错误'))
        if not params.get('limit') or not params['limit'].isdigit():
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='条数错误'))
        params['limit'] = int(params['limit'])
        params['page'] = (int(params['page']) - 1) * params['limit']
        params["role_type"], params["role_regions"] = SessionOperationClass.get_locations()

        return Response(params=params)


class BusinessMsgOperation(Resource):
    @doc.request_business_msg_post
    @operations.BusinessMsgList.put_msg(params=dict)
    def put(self, msg_id):
        params = get_payload()
        params['msg_id'] = int(msg_id)
        params['follow_name'] = str(params.get('follow_name') or '')
        params['follow_result'] = str(params.get('follow_result') or '')
        return Response(params=params)


ns = api.namespace('business_msg', description='物流商业信息')
ns.add_resource(BusinessMsg, '/business_msg/')
ns.add_resource(BusinessMsgOperation, '/business_msg/<int:msg_id>')
