import json

from server.meta.decorators import make_decorator
from server.status import build_result, HTTPStatus, APIStatus, make_result
from server.utils.date_format import get_date_aggregate

class UserList(object):

    @staticmethod
    @make_decorator
    def get(user_list):
        # 过滤字段
        user_list = json.loads(json.dumps(user_list))
        user_detail = user_list['user_detail']
        for detail in user_detail:
            # 认证
            role_auth = []
            if detail['auth_goods']:
                role_auth.append('货主')
            if detail['auth_driver']:
                role_auth.append('司机')
            if detail['auth_company']:
                role_auth.append('物流公司')
            detail['role_auth'] = ','.join(role_auth) if role_auth else '未认证'
            detail.pop('auth_goods')
            detail.pop('auth_driver')
            detail.pop('auth_company')

            detail['usual_city'] = detail['usual_city'] if detail['usual_city'] else '未知常驻地'

        return build_result(APIStatus.Ok, count=user_list['user_count'], data=user_detail), HTTPStatus.Ok


class UserStatistic(object):

    @staticmethod
    @make_decorator
    def get_result(params, data, before_user_count):
        # 日期聚合
        xAxis, series = get_date_aggregate(params['start_time'], params['end_time'], params['periods'], data, date_field='create_time', number_field='count')
        # 累计
        if params['user_type'] != 1:
            series = [sum(series[: i+1]) + before_user_count if i > 0 else series[i] + before_user_count for i in range(len(series))]
        # 按月分段，返回总和
        if params['periods'] == 4:
            data = {'xAxis': xAxis, 'series': series, 'last_month': sum(series)}
        else:
            data = {'xAxis': xAxis, 'series': series}
        return make_result(APIStatus.Ok, data=data), HTTPStatus.Ok