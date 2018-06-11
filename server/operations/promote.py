# -*- coding: utf-8 -*-
from flask_restful import abort

from server.database import db, mongo
from server.meta.decorators import make_decorator, Response
from server.models import RegionsModel
from server.models.promote import PromoteEffectList, PromoteQuality
from server.status import HTTPStatus, make_result, APIStatus


class PromoteEffectDecorator(object):

    @staticmethod
    @make_decorator
    def get_promote_effect_list(page, limit, params):
        data = PromoteEffectList.get_promote_effect_list(db.read_bi, page, limit, params)

        return Response(data=data)

    @staticmethod
    @make_decorator
    def add_extension_worker(mobile):
        # 校验该mobile是否在user表中并且该mobile的主人现在不是推荐人
        user_name, user_id, reference_id = PromoteEffectList.check_mobile(db.read_bi, mobile)
        if user_id and not reference_id:
            data = PromoteEffectList.add_extension_worker(db.read_bi, user_name, user_id, mobile)
        else:
            data = 0

        return Response(data=data)

    @staticmethod
    @make_decorator
    def delete_from_tb_inf_promte(reference_id):
        data = PromoteEffectList.delete_from_tb_inf_promte(db.read_bi, reference_id)
        return Response(data=data)



class PromoteQualityDecorator(object):

    @staticmethod
    @make_decorator
    def get_promote_quality(params):
        # 地区
        # user_id = []
        # if params['region_id']:
        #     three_region = RegionsModel.get_three_area(db.read_db, params['region_id'])
        #     if not three_region:
        #         abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='地区选择错误'))
        #     if three_region['first_code']:
        #         region = {
        #             'province_id': three_region['first_code'],
        #             'city_id': three_region['second_code'],
        #             'county_id': three_region['third_code']
        #         }
        #     else:
        #         region = {
        #             'province_id': three_region['second_code'],
        #             'city_id': three_region['third_code']
        #         }
        #     result = mongo.user_locations.collection.aggregate([{
        #         '$match': region
        #     },
        #         {'$group': {'_id': {'province_id': '$province_id', 'city_id': '$city_id', 'county_id': '$county_id'},
        #                     'scores': {'$addToSet': '$user_id'}}
        #          }])
        #     for i in result:
        #         user_id.extend(i['scores'])
        #     user_id = list(set(user_id))

        # 新增
        promote_quality = PromoteQuality.get_promote_quality(db.read_bi, params)
        # 之前累计
        before_promote_count = PromoteQuality.get_before_promote_count(db.read_bi, params)
        return Response(params=params, data=promote_quality, before_promote_count=before_promote_count)
