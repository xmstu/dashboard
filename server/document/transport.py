from server import api

transport_radar_param = api.doc(params={
    "start_time": "开始时间",
    "end_time": "开始时间",
    "region_id": "地区id",
    "business": "业务:1.同城;2.跨城"
}, description='运力趋势查询参数')

transport_list_param = api.doc(params={
    "from_province_id": "出发地省份id",
    "from_city_id": "出发地城市id",
    "from_county_id": "出发地区县id",
    "from_town_id": "出发地城镇id",
    "to_province_id": "目的地省份id",
    "to_city_id": "目的地城市id",
    "to_county_id": "目的地区县id",
    "to_town_id": "目的地城镇id",
    "vehicle_length": "车长要求",
    "business": "业务类型:1.同城;2.跨城",
    "filter": "筛选条件:1.货源>车辆;2.货源<车辆;",
    "start_time": "开始时间",
    "end_time": "结束时间",
}, description='运力列表查询参数')
