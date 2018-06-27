from server import api

transport_trend_param = api.doc(params={
    "start_time":"开始时间",
    "end_time":"开始时间",
    "periods":"按日,按周,按月",
    "region_id":"地区id",
    "business":"业务:1.同城;2.跨城",
    "vehicle":"车长要求"
}, description='运力趋势查询参数')
