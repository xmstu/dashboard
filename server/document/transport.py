from server import api

transport_radar_param = api.doc(params={
    "start_time":"开始时间",
    "end_time":"开始时间",
    "region_id":"地区id",
    "business":"业务:1.同城;2.跨城"
}, description='运力趋势查询参数')
