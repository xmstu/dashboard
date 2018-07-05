from server import api

heat_map_param = api.doc(params={
    "dimension": "1.按用户;2.按货源;3.按车型",
    "filter": "用户:1.司机/2.货主;货源:1.同城/2.跨城;车长:1.小面包车/4.2米等",
    "field": "用户:1.用户数/2.认证数/3.活跃数;货源:1.货源数/2.货源金额/3.订单数/4.订单金额;车型:1.货源所需/2.车辆数/3.实际接单",
    "start_time": "开始时间",
    "end_time": "开始时间",
}, description='运力趋势查询参数')