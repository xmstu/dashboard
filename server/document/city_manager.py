# -*- coding: utf-8 -*-

from server import api

request_city_manager = api.doc(params={
    'mobile': '手机号',
    'start_time': '开始日期(时间戳),默认:8天前',
    'end_time': '结束日期(时间戳),默认:昨天',
})