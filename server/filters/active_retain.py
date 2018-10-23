from server.meta.decorators import make_decorator
from server.status import make_resp, APIStatus, HTTPStatus
from server.utils.date_format import get_date_aggregate


class ActiveUserStatistic(object):
    @staticmethod
    @make_decorator
    def get_active_user_statistic(params, data):
        xAxis, count_series = get_date_aggregate(params["start_time"], params["end_time"], params["periods"], data)
        ret = {
            "xAxis": xAxis,
            "count_series": count_series,
        }
        return make_resp(status=APIStatus.Ok, data=ret), HTTPStatus.Ok

