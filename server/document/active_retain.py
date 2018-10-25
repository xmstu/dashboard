from server import api

request_user_retain_statistic_param = api.doc(params={
    'start_time': '开始日期(时间戳),默认:7天前',
    'end_time': '结束日期(时间戳),默认:当前时间',
    'periods': '时间周期,2:日，3:周，4:月，默认:2',
    'user_type': '用户类型,1:货主，2:司机，3:物流公司，默认:0',
    'special_tag': '1.不计算当天住处;默认:0',
    'region_id': '地区id',
    }, description='用户行为变化趋势查询参数')

request_user_retain_list_param = api.doc(params={
    'start_date': '开始日期(字符串),默认:7天前',
    'end_date': '结束日期(字符串),默认:当前时间',
    'user_type': '用户类型,1:货主，2:司机，3:物流公司，默认:0',
    'user_behavior': '用户行为1:登录,2:发货,3:接单,默认:1',
    'region_id': '地区id',
    }, description='用户行为变化趋势查询参数')
