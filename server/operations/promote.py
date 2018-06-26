# -*- coding: utf-8 -*-
from flask_restful import abort

from server.database import db
from server.logger import log
from server.meta.decorators import make_decorator, Response
from server.models.promote import PromoteEffectList, get_new_users, get_user_behavior, get_money
from server.status import HTTPStatus, make_result, APIStatus

class PromoteEffectDecorator(object):

    @staticmethod
    @make_decorator
    def get_promote_effect_list(page, limit, params):
        # 城市经理只能查询自己手下
        if params['role'] == 4:
            # 城市经理手下
            promote_users = PromoteEffectList.get_extension_info(db.read_bi, params['user_id'])
            if not promote_users:
                return
            # 推广人员
            user_id, count = PromoteEffectList.get_extension_worker(db.read_bi, page, limit, params, promote_users)
        else:
            # 所有推广人员
            user_id, count = PromoteEffectList.get_extension_worker(db.read_bi, page, limit, params)

        return Response(extension_worker_list=extension_worker_list, promote_effect_list=promote_effect_list, params=params)

    @staticmethod
    @make_decorator
    def add_extension_worker(user_id, mobile, admin_type):
        # 查询推广人员
        promoter_id = PromoteEffectList.check_extension_mobile(db.read_db, mobile)
        # 校验该推广人员注册且不是推荐人
        if not promoter_id or user_id == promoter_id:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='推广人员未注册或为推荐人'))
        # 是否存在
        if PromoteEffectList.check_promote_alive(db.read_bi, promoter_id):
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='该推广人员已存在'))
        # 添加推广人员
        result = PromoteEffectList.add_extension_worker(db.read_bi, user_id, promoter_id, admin_type)

        return Response(result=result)

    @staticmethod
    @make_decorator
    def delete_from_tb_inf_promte(user_id, admin_type, promoter_id):
        data = PromoteEffectList.delete_from_tb_inf_promte(db.read_bi, user_id, admin_type, promoter_id)
        return Response(data=data)


class PromoteQualityDecorator(object):

    @staticmethod
    @make_decorator
    def get_promote_quality(params):
        try:
            # 数据源未更新，先用业务库
            promote_quality = []
            before_promote_count = 0
            # 拉新 - 新增 累计
            if params['dimension'] == 1:
                promote_quality, before_promote_count = get_new_users(db.read_db, params)
            # 用户行为 - 登录 发货 接单 完成订单
            elif params['dimension'] == 2:
                promote_quality = get_user_behavior(db.read_db, params)
            # 金额
            elif params['dimension'] == 3:
                promote_quality = get_money(db.read_db, params)
            return Response(params=params, data=promote_quality, before_promote_count=before_promote_count)
        except Exception as e:
            log.error('推荐人质量统计异常: [error: %s]' % e)
