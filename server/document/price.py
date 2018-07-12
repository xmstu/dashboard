from server import api

price_trend_param = api.doc(params={
    "from_province_id": "出发地省份",
    "from_city_id": "出发地城市",
    "from_county_id": "出发地区县",
    "to_province_id": "目的地省份",
    "to_city_id": "目的地城市",
    "to_county_id": "目的地区县",
    "min_mileage": "最小里程",
    "max_mileage": "最大里程",
    "vehicle_length": "车型",
    "pay_method": "1.线上支付;2.线下支付",
    "start_time": "开始时间",
    "end_time": "结束时间",
    "periods": "1.按日;2.按周;3.按月",
}, description='价格趋势统计')
