from server.cache_data import init_regions
from server.status import HTTPStatus, APIStatus, make_resp
from server.utils.date_format import get_date_aggregate


def user_list_get_result(user_list):
    user_detail = user_list['user_detail']

    def filter_user_info(detail):
        # 用户类型
        user_type = ''
        if detail['user_type'] == 1:
            user_type = '货主'
        elif detail['user_type'] == 2:
            user_type = '司机'
        elif detail['user_type'] == 3:
            user_type = '公司'
        # 认证
        role_auth_arr = []
        if detail['goods_auth']:
            role_auth_arr.append('货主')
        if detail['driver_auth']:
            role_auth_arr.append('司机')
        if detail['company_auth']:
            role_auth_arr.append('公司')
        role_auth = ','.join(role_auth_arr) if role_auth_arr else '未认证'
        detail_dict = {
            'user_id': detail['user_id'],
            'user_name': detail['user_name'],
            'mobile': detail['mobile'],
            'user_type': user_type,
            'role_auth': role_auth,
            'goods_count': detail['goods_count_SH'] + detail['goods_count_LH'],
            'order_count': detail['order_count_SH'] + detail['order_count_LH'],
            'order_finished_count': detail['order_finished_count_SH_online'] + detail[
                'order_finished_count_SH_unline'] + detail['order_finished_count_LH_online'] + detail[
                                        'order_finished_count_LH_unline'],
            'download_channel': detail['download_channel'],
            'from_channel': detail['from_channel'],
            'last_login_time': detail['last_login_time'],
            'create_time': detail['create_time'],
            'usual_city': init_regions.to_address(detail['from_province_id'], detail['from_city_id'],
                                                  detail['from_county_id'])
        }
        return detail_dict

    result = []
    for detail in user_detail:
        result.append(filter_user_info(detail))

    return make_resp(APIStatus.Ok, count=user_list['user_count'], data=result), HTTPStatus.Ok


def user_statistic_get_result(params, data, before_user_count):
    # 日期聚合
    xAxis, series = get_date_aggregate(params['start_time'], params['end_time'], params['periods'], data,
                                       date_field='create_time', number_field='count')
    # 累计
    if params['user_type'] != 1:
        series = [sum(series[: i + 1]) + before_user_count if i > 0 else series[i] + before_user_count for i in
                  range(len(series))]
    # 按月分段，返回总和
    if params['periods'] == 4:
        data = {'xAxis': xAxis, 'series': series, 'last_month': sum(series)}
    else:
        data = {'xAxis': xAxis, 'series': series}
    return make_resp(APIStatus.Ok, data=data), HTTPStatus.Ok


def get_behavior_result(params, data):
    xAxis, count_series = get_date_aggregate(params["start_time"], params["end_time"], params["periods"], data)
    ret = {
        "xAxis": xAxis,
        "count_series": count_series,
    }
    return make_resp(APIStatus.Ok, data=ret), HTTPStatus.Ok
