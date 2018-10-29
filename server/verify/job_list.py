from flask_restful import abort

from server import log
from server.status import HTTPStatus, make_resp, APIStatus


def check_jobs_list(params):

    try:
        params["job_name"] = str(params.get("job_name", ''))
        params["region"] = str(params.get("region") or '')
        params["time_scale"] = int(params.get("time_scale") or 0)
        params["page"] = int(params.get("page") or 1)

        return params

    except Exception as e:
        log.error('查询职位列表出现错误 [Error: %s]' % e)
        abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='查询职位列表出现错误'))
