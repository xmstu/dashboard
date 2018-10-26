import datetime
import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.status import HTTPStatus, make_resp, APIStatus
from server.utils.extend import compare_time, complement_time
from server.utils.role_regions import get_role_regions


class ActiveUserStatistic(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            params["start_time"] = int(params.get("start_time") or time.time()-86400*7)
            params["end_time"] = int(params.get("end_time") or time.time())
            params["periods"] = int(params.get("periods") or 2)
            params["user_type"] = int(params.get("user_type") or 0)
            params["special_tag"] = int(params.get("special_tag") or 0)
            params["region_id"] = int(params.get("region_id") or 0)

            # 当前权限下所有地区
            params['region_id'] = get_role_regions(params['region_id'])

            # 补全时间
            params['start_time'], params['end_time'] = complement_time(params['start_time'], params['end_time'])

            # 校验参数
            if not compare_time(params['start_time'], params['end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='时间参数有误'))
            log.info("留存趋势请求参数 [params: {}]".format(params))
            return Response(params=params)
        except Exception as e:
            log.error('留存趋势请求参数非法:[Error:%s]' % e)
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='留存趋势请求参数非法'))


def active_user_list_check_params(params):
    try:
        params["start_date"] = int(params.get("start_date") or time.time() - 7 * 86400)
        params["end_date"] = int(params.get("end_date") or time.time())
        params["user_type"] = int(params.get("user_type") or 0)
        params["user_behavior"] = int(params.get("user_behavior") or 1)
        params['region_id'] = int(params.get('region_id') or 0)

        # 当前权限下所有地区
        params['region_id'] = get_role_regions(params['region_id'])

        # 开始日期和结束日期
        params["start_date"] = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(params["start_date"])), "%Y-%m-%d")
        params["end_date"] = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(params["end_date"])), "%Y-%m-%d")
        if params["start_date"] > params["end_date"]:
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='开始日期必须小于结束日期'))
        log.info("留存列表请求参数 [params: {}]".format(params))
        return params
    except Exception as e:
        log.error('留存列表请求参数非法 [Error: %s]' % e)
        abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='留存列表请求参数非法'))