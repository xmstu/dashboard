from server import api

transport_radar_param = api.doc(params={
    "start_time": "开始时间",
    "end_time": "开始时间",
    "region_id": "地区id",
    "from_province_id": "出发地省份id",
    "from_city_id": "出发地城市id",
    "from_county_id": "出发地区县id",
    "from_town_id": "出发地城镇id",
    "to_province_id": "目的地省份id",
    "to_city_id": "目的地城市id",
    "to_county_id": "目的地区县id",
    "to_town_id": "目的地城镇id",
}, description='运力趋势查询参数')

transport_list_param = api.doc(params={
    "from_city_id": "出发地城市id",
    "to_city_id": "目的地城市id",
    "start_time": "统计时间,传当前选择日期00:00:00的时间戳",
    "calc_town": "0:不计算区镇;1:计算出发地城市下所有区镇;2.计算目的地城市下所有区镇",
    "page": "页数",
    "limit": "条数",
}, description='运力列表查询参数')
