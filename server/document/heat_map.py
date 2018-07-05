from server import api

heat_map_param = api.doc(params={
    "dimension": "1.按用户;2.按货源;3.按车型",
    "data_type": "用户:司机/货主;货源:同城/跨城;车长:小面包车/4.2米等",
    "start_time": "开始时间",
    "end_time": "开始时间",
}, description='运力趋势查询参数')