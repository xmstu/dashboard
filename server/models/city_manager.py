# -*- coding: utf-8 -*-

class cityManagerModel(object):
    @staticmethod
    def get_promoter(cursor, mobile):
        """获取推广人员"""
        command = '''
        SELECT tb_inf_promoter.mobile
        FROM tb_inf_city_manager
        INNER JOIN tb_inf_promoter ON tb_inf_city_manager.id = tb_inf_promoter.manager_id
        AND tb_inf_promoter.is_deleted = 0
        
        WHERE tb_inf_city_manager.is_deleted = 0 AND tb_inf_city_manager.account = :mobile '''

        result = cursor.query(command, {
            'mobile': mobile
        })

        return result if result else []

    @staticmethod
    def increased_user_data(cursor, user_ids, start_time, end_time):
        command = '''
        SELECT recommended_user_id,
        -- 司机认证
        shu_user_auths.auth_driver,
        -- 发货数
        (SELECT IF(COUNT(*) >= 5, 5, COUNT(*))
        FROM shf_goods
        WHERE create_time >= :start_time
        AND create_time <= :end_time
        AND user_id = shu_recommended_users.recommended_user_id
        ) AS goods_count,
        -- 在线支付订单数
        (SELECT IF(COUNT(*) >= 5, 5, COUNT(*))
        FROM shb_orders
        INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id
        AND shf_goods.is_deleted = 0
        AND shf_goods.`status` != -1
        AND shb_orders.is_deleted = 0
        AND shb_orders.`status` = 3
        AND shb_orders.pay_status = 2
        WHERE shb_orders.create_time >= :start_time
        AND shb_orders.create_time <= :end_time
        AND shb_orders.owner_id = shu_recommended_users.recommended_user_id
        ) AS order_count
        
        FROM shu_recommended_users
        INNER JOIN shu_users ON shu_recommended_users.referrer_user_id = shu_users.id
        AND shu_users.is_deleted = 0
        INNER JOIN shu_user_profiles ON shu_users.id = shu_user_profiles.user_id
        LEFT JOIN shu_user_auths ON shu_user_profiles.last_auth_driver_id = shu_user_auths.id
        AND shu_user_auths.auth_status = 2 AND shu_user_auths.is_deleted = 0
        AND shu_user_auths.submit_time >= :start_time AND shu_user_auths.submit_time <= :end_time
        WHERE shu_users.mobile IN (:user_ids)'''

        result = cursor.query(command, {
            'user_ids': user_ids,
            'start_time': start_time,
            'end_time': end_time
        })

        return result if result else []