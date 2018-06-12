# -*- coding: utf-8 -*-

from flask_restplus import Resource
from flask import request

from server.meta.decorators import Response
from server import api
from server import operations, filters

class Weather(Resource):
    @staticmethod
    @filters.weather.Weather.get_result(data=dict)
    @operations.weather.WeatherDecorator.get_city(ip=str)
    def get():
        """ip所在城市信息"""
        ip = request.remote_addr
        resp = Response(ip=ip)
        return resp

ns = api.namespace('weather', description='获取所在城市接口')
ns.add_resource(Weather, '/')