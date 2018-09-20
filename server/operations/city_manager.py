# -*- coding: utf-8 -*-

from server.meta.decorators import make_decorator, Response
from server.models.city_manager import cityManagerModel
from server.database import db

class cityManagerOperation(object):
    @staticmethod
    @make_decorator
    def get_city_manager_data(params):
        """获取城市经理提成数据"""
        result = cityManagerModel.increased_user_data(db.read_db, params['mobile'], params['start_time'], params['end_time'])
        return Response(data=result)