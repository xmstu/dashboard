from server import api


verify_vehicle_list_param = api.doc(params={
    "mobile": "手机号",
    "vehicle_number": "车牌号码",
    "home_station_province_id": "常驻地省份id",
    "home_station_city_id": "常驻地城市id",
    "home_station_county_id": "常驻地区县id",
    "vehicle_length": "车长要求",
    "verify_start_time": "认证开始时间",
    "verify_end_time": "认证结束时间",
    "last_login_start_time": "最后登录开始时间",
    "last_login_end_time": "最后登录结束时间",
    "page": "页数",
    "limit": "条数",
}, description='运力列表查询参数')