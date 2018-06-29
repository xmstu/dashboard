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
            return Response(result=[], count=0, params=params)
        # 推广列表
        result = PromoteEffectList.get_promote_list(db.read_bi, params, referrer_mobile)

        return Response(result=result, count=count, params=params)

    @staticmethod
    @make_decorator
    def add_extension_worker(user_id, mobile, user_name):
        """添加推广人员"""
        try:
            # 推广人员是否存在
            is_alive = PromoteEffectList.check_promoter(db.read_bi, user_id, mobile)
            if not is_alive:
                # 添加推广人员
                result = PromoteEffectList.add_promoter(db.read_bi, user_id, mobile, user_name)
                return Response(result=result)
            return Response(result=0)
        except Exception as e:
            log.error('添加推广人员失败: [error: %s]' % e)

    @staticmethod
    @make_decorator
    def delete_promoter(user_id, promoter_id):
        """删除推广人员"""
        try:
            result = PromoteEffectList.delete_promoter(db.read_bi, user_id, promoter_id)
            return Response(result=result)
        except Exception as e:
            log.error('删除推广人员失败: [error: %s]' % e)


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
