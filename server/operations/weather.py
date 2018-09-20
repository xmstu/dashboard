# -*- coding: utf-8 -*-

from server import log
from server.meta.decorators import make_decorator, Response
from server.status import make_resp, HTTPStatus, APIStatus

import requests
from flask_restful import abort

class WeatherDecorator(object):
    @staticmethod
    @make_decorator
    def get_city(ip):
        url = 'http://api.map.baidu.com/location/ip?ak=ZVizfVIbcLc0qNhduvT3dSbqG8YV8YoP&ip=%s' % ip
        for _ in range(5):
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    if r.json()['status'] == 1:
                        return Response(data={})
                    else:
                        return Response(data=r.json())
                return Response(data={})
            except Exception as e:
                log.warn('请求百度接口异常: [error: %s]' % e, exc_info=True)
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='参数有误'))