# -*- coding: utf-8 -*-
from flask_restful import abort

from server.database import db
from server.logger import log
from server.meta.decorators import make_decorator, Response
from server.models.promote import PromoteQuality, PromoteEffectList
from server.status import HTTPStatus, make_result, APIStatus

class PromoteEffectDecorator(object):

    @staticmethod
    @make_decorator
    def get_promote_effect_list(page, limit, params):
        # 城市经理
        if params['role'] == 4:
            promoter_mobile = PromoteEffectList.get_promoter_mobile_by_city_manage(db.read_bi, params)
        else:
            promoter_mobile = PromoteEffectList.get_promoter_mobile_by_admin(db.read_bi, params)
        # 推广人员数量即为总数
        count = len(promoter_mobile)
        referrer_mobile = promoter_mobile[(page-1)*limit:page*limit+1]
        if count == 0:
            return
        # 推广列表
        result = PromoteEffectList.get_promote_list(db.read_bi, params, referrer_mobile)

        return Response(result=result, count=count, params=params)

    @staticmethod
    @make_decorator
    def add_extension_worker(user_id, mobile, admin_type):
        pass

    @staticmethod
    @make_decorator
    def delete_from_tb_inf_promte(user_id, admin_type, promoter_id):
        pass


class PromoteQualityDecorator(object):

    @staticmethod
    @make_decorator
    def get_promote_quality(params):
        try:
            promoter_ids = []
            before_promote_count = 0
            promote_quality = []
            # 城市经理
            if params['role'] == 4:
                promoter_mobile = PromoteQuality.get_promoter_mobile(db.read_bi, params['user_id'])
                promoter_ids = PromoteQuality.get_promoter_id(db.read_db, promoter_mobile)
            # 拉新 - 新增 累计
            if params['dimension'] == 1:
                promote_quality, before_promote_count = PromoteQuality.get_new_users(db.read_db, params, promoter_ids)
            # 用户行为 - 登录 发货 接单 完成订单
            elif params['dimension'] == 2:
                promote_quality = PromoteQuality.get_user_behavior(db.read_db, params, promoter_ids)
            # 金额
            elif params['dimension'] == 3:
                promote_quality = PromoteQuality.get_money(db.read_db, params, promoter_ids)
            return Response(params=params, data=promote_quality, before_promote_count=before_promote_count)
        except Exception as e:
            log.error('推荐人质量统计异常: [error: %s]' % e)
