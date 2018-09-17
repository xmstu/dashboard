from server import api

distribution_map_param = api.doc(params={
    "dimension": "1.按用户;2.按货源;3.按运力;4.按订单",
    "filter": "用户:1.司机/2.货主/3.物流公司;货源:1.议价/2.一口价;运力:1.小面包车/4.2米等;订单:1.议价/2.一口价",
    "field": "用户:1.新增用户数/2.累计用户数/3.累计认证数/4.登陆过/5.均有登录;"
             "货源:1.货源数/2.接单数/3.取消数/4.待接单;"
             "车型:1.货源所需/2.累计车辆数/3.活跃车辆数;"
             "订单:1.订单数/2.完成数/3.进行中/4.已取消",
    "start_time": "开始时间",
    "end_time": "开始时间",
    "region_id": "地区id"
}, description='分布图查询参数')

goods_map_param = api.doc(params={
    "goods_price_type": "0.全部;1.一口价;2.议价;",
    "haul_dist": "0.全部;1.同城;2.跨城;",
    "vehicle_length": "空字符串:全部;常用车型:4.2米,5.2米等",
    "goods_status": "0.全部;1.待接单;2.已接单;3.已完成;4.已取消",
    "special_tag": "0.全部;1.新用户",
    "delivery_start_time": "开始发货时间",
    "delivery_end_time": "结束发货时间",
    "register_start_time": "开始注册时间",
    "register_end_time": "结束注册时间",
}, description='货源热力图查询参数')

users_map_param = api.doc(params={
    "goods_price_type": "0.全部;1.一口价;2.议价;",
    "haul_dist": "0.全部;1.同城;2.跨城;",
    "vehicle_length": "空字符串:全部;常用车型:4.2米,5.2米等",
    "goods_status": "0.全部;1.待接单;2.已接单;3.已完成;4.已取消",
    "special_tag": "0.全部;1.新用户",
    "delivery_start_time": "开始发货时间",
    "delivery_end_time": "结束发货时间",
    "register_start_time": "开始注册时间",
    "register_end_time": "结束注册时间",
}, description='用户热力图查询参数')
