# -*- coding: utf-8 -*-

from server.meta.decorators import make_decorator, Response
from server.models.city_manager import cityManagerModel
from server.database import db

class cityManagerOperation(object):
    @staticmethod
    @make_decorator
    def get_city_manager_data(params):
        """获取城市经理提成数据"""
        # 获取城市经理手下推广人员
        promoter = cityManagerModel.get_promoter(db.read_bi, params['mobile'])
        promoter_ids = [str(i['mobile']) for i in promoter if i.get('mobile')]
        if not promoter_ids:
            return Response(data=[])
        # 获取新增用户
        result = cityManagerModel.increased_user_data(db.read_db, ','.join(promoter_ids), params['start_time'], params['end_time'])
        return Response(data=result)