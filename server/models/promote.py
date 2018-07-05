# -*- coding: utf-8 -*-
import time

from flask_restful import abort

from server import log
from server.status import HTTPStatus, make_result, APIStatus


class PromoteEffectList(object):
    @staticmethod
    def get_promoter_mobile_by_city_manage(cursor, params):
        """城市经理获取推广人员信息"""
        command = """
        SELECT tb_inf_promoter.mobile
        FROM tb_inf_city_manager
        LEFT JOIN tb_inf_promoter ON tb_inf_city_manager.id = tb_inf_promoter.manager_id AND tb_inf_promoter.is_deleted = 0

        WHERE tb_inf_city_manager.id = :user_id
        %s
        AND tb_inf_city_manager.is_deleted = 0
        """
        fetch_where = ''
        # 用户名
        if params['user_name']:
            fetch_where += "AND tb_inf_promoter.user_name = '%s' " % params['user_name']
        # 手机号
        if params['mobile']:
            fetch_where += "AND tb_inf_promoter.mobile = '%s' " % params['mobile']

        command = command % fetch_where
        result = cursor.query(command, {'user_id': params['user_id']})

        return [i['mobile'] for i in result if i['mobile']] if result else []

    @staticmethod
    def get_promoter_mobile_by_admin(cursor, params):
        """其他人获取推广人员"""
        command = """
        SELECT mobile
        FROM tb_inf_user
        WHERE is_deleted = 0
        AND mobile IN (
        SELECT DISTINCT referrer_mobile
        FROM tb_inf_user
        WHERE referrer_mobile != '')
        %s
        """
        fetch_where = ''
        # 用户名
        if params['user_name']:
            fetch_where += "AND user_name = '%s' " % params['user_name']
        # 手机号
        if params['mobile']:
            fetch_where += "AND mobile = '%s' " % params['mobile']

        command = command % fetch_where
        result = cursor.query(command)

        return [i['mobile'] for i in result if i['mobile']] if result else []

    @staticmethod
    def get_promote_list(cursor, params, referrer_mobile):
        """获取推广人员列表"""
        command = '''
        SELECT
        
        referrer.*,
        COUNT(*) AS user_count,
        0 AS wake_up_count,
        IF(SUM(goods_count_SH), SUM(goods_count_SH), 0) AS goods_count_SH,
        IF(SUM(goods_count_LH), SUM(goods_count_LH), 0) AS goods_count_LH,
        (SELECT COUNT(DISTINCT user_id) FROM tb_inf_user WHERE goods_count_SH > 0 AND referrer_mobile = referrer.mobile) AS goods_user_count_SH,
        (SELECT COUNT(DISTINCT user_id) FROM tb_inf_user WHERE goods_count_LH > 0 AND referrer_mobile = referrer.mobile) AS goods_user_count_SH,
        (SELECT COUNT(DISTINCT user_id) FROM tb_inf_user WHERE (goods_count_SH > 0 OR goods_count_LH > 0) AND referrer_mobile = referrer.mobile) AS goods_user_count,
        IF(SUM(order_finished_count_SH_online), SUM(order_finished_count_SH_online), 0) AS order_over_count_SH_online,
        IF(SUM(order_finished_count_SH_unline), SUM(order_finished_count_SH_unline), 0) AS order_over_count_SH_unline,
        IF(SUM(order_finished_count_LH_online), SUM(order_finished_count_LH_online), 0) AS order_over_count_LH_online,
        IF(SUM(order_finished_count_LH_unline), SUM(order_finished_count_LH_unline), 0) AS order_over_count_LH_unline,
        IF(SUM(goods_price_SH), SUM(goods_price_SH), 0) AS goods_price_SH,
        IF(SUM(goods_price_LH), SUM(goods_price_LH), 0) AS goods_price_LH,
        IF(SUM(order_over_price_SH_online), SUM(order_over_price_SH_online), 0) AS order_over_price_SH_online,
        IF(SUM(order_over_price_SH_unline), SUM(order_over_price_SH_unline), 0) AS order_over_price_SH_unline,
        IF(SUM(order_over_price_LH_online), SUM(order_over_price_LH_online), 0) AS order_over_price_LH_online,
        IF(SUM(order_over_price_LH_unline), SUM(order_over_price_LH_unline), 0) AS order_over_price_LH_unline
        
        -- 推广人
        FROM (
        SELECT user_id, IF(tb_inf_promoter.user_name != '', tb_inf_promoter.user_name, tb_inf_user.user_name) AS user_name, tb_inf_user.mobile
        FROM tb_inf_user
        LEFT JOIN tb_inf_promoter ON tb_inf_user.mobile = tb_inf_promoter.mobile AND tb_inf_promoter.is_deleted = 0
        WHERE tb_inf_user.mobile IN (%s)) AS referrer
        -- 推广信息
        LEFT JOIN tb_inf_user ON referrer.mobile = tb_inf_user.referrer_mobile
        WHERE 1=1 %s
        GROUP BY referrer.user_id
        '''

        mobile = ','.join(["'"+i+"'" for i in referrer_mobile])
        fetch_where = ''
        # 推荐角色
        if params['role_type']:
            fetch_where += 'AND tb_inf_user.user_type = %s ' % params['role_type']
        # 是否活跃
        if params['is_actived'] == 1:
            fetch_where += 'AND tb_inf_user.keep_login_days >= 7 AND tb_inf_user.last_login_time > UNIX_TIMESTAMP() - 1 * 86400 '
        elif params['is_actived'] == 2:
            fetch_where += '''AND tb_inf_user.last_login_time < UNIX_TIMESTAMP() - 1 * 86400
            AND tb_inf_user.last_login_time > UNIX_TIMESTAMP() - 3 * 86400 '''
        elif params['is_actived'] == 3:
            fetch_where += '''AND tb_inf_user.last_login_time < UNIX_TIMESTAMP() - 4 * 86400
            AND tb_inf_user.last_login_time > UNIX_TIMESTAMP() - 10 * 86400 '''
        elif params['is_actived'] == 4:
            fetch_where += '''AND tb_inf_user.last_login_time < UNIX_TIMESTAMP() - 10 * 86400 '''
        # 贴车贴
        if params['is_car_sticker'] == 1:
            fetch_where += 'AND tb_inf_user.is_sticker = 1 '
        elif params['is_car_sticker'] == 2:
            fetch_where += 'AND tb_inf_user.is_sticker = 0 '
        # 注册日期
        if params['start_time'] and params['end_time']:
            fetch_where += 'AND tb_inf_user.create_time > %s AND tb_inf_user.create_time <= %s ' % (params['start_time'], params['end_time'])

        command = command % (mobile, fetch_where)

        result = cursor.query(command)
        return result if result else []

    @staticmethod
    def check_promoter(cursor, user_id, mobile):
        """检查推广人员是否存在"""
        command = '''
        SELECT tb_inf_city_manager.id
        FROM tb_inf_city_manager
        LEFT JOIN tb_inf_promoter ON tb_inf_city_manager.id = tb_inf_promoter.manager_id AND tb_inf_promoter.is_deleted = 0
        WHERE tb_inf_city_manager.id = :user_id AND tb_inf_city_manager.is_deleted = 0
        AND tb_inf_promoter.mobile = :mobile '''

        result = cursor.query_one(command, {'user_id': user_id, 'mobile': mobile})

        return result['id'] if result else None

    @staticmethod
    def add_promoter(cursor, user_id, mobile, user_name):
        """添加推广人员"""
        try:
            command = '''
            INSERT INTO tb_inf_promoter(manager_id, user_name, mobile)
            VALUES (:manager_id, :user_name, :mobile)
            '''
            result = cursor.insert(command, {
                'manager_id': user_id,
                'mobile': mobile,
                'user_name': user_name
            })

            return result
        except Exception as e:
            log.error('添加推广人员失败: [user_id: %s][user_name: %s][mobile: %s][error: %s]' % (user_id, user_name, mobile, e), exc_info=True)

    @staticmethod
    def delete_promoter(cursor, user_id, promoter_id):
        """删除推广人员"""
        command = '''
        UPDATE tb_inf_promoter, tb_inf_user
        SET tb_inf_promoter.is_deleted = 1
        WHERE tb_inf_promoter.manager_id = :user_id AND tb_inf_promoter.mobile = tb_inf_user.mobile
        AND tb_inf_user.user_id = :promoter_id
        '''
        result = cursor.update(command, {
            'user_id': user_id,
            'promoter_id': promoter_id
        })

        return result

class PromoteQuality(object):
    @staticmethod
    def get_promoter_mobile_by_city_manager(cursor, user_id):
        """城市经理获取推广人员信息"""
        command = """
        SELECT tb_inf_promoter.mobile
        FROM tb_inf_city_manager
        LEFT JOIN tb_inf_promoter ON tb_inf_city_manager.id = tb_inf_promoter.manager_id AND tb_inf_promoter.is_deleted = 0

        WHERE tb_inf_city_manager.id = :user_id
        AND tb_inf_city_manager.is_deleted = 0
        """
        result = cursor.query(command, {'user_id': user_id})

        return [i['mobile'] for i in result if i['mobile']] if result else []

    @staticmethod
    def get_promoter_mobile_by_admin(cursor):
        """管理员获取推广人员信息"""
        command = """
        SELECT mobile
        FROM tb_inf_promoter
        WHERE is_deleted = 0
        """
        result = cursor.query(command)

        return [i['mobile'] for i in result if i['mobile']] if result else []

    @staticmethod
    def get_promoter_mobile_by_suppliers(cursor, city_region):
        """区镇合伙人获取推广人员信息"""
        if not city_region:
            return []
        command = """
        SELECT tb_inf_promoter.mobile
        FROM tb_inf_city_manager
        INNER JOIN tb_inf_promoter ON tb_inf_city_manager.id = tb_inf_promoter.manager_id AND tb_inf_promoter.is_deleted = 0
        WHERE tb_inf_city_manager.is_deleted = 0
        AND tb_inf_city_manager.region_id IN (%s)
        """
        command = command % ','.join([str(i) for i in city_region])
        result = cursor.query(command)

        return [i['mobile'] for i in result if i['mobile']] if result else []

    @staticmethod
    def get_promoter_id(cursor, mobile):
        """推广人员id"""
        command = """
        SELECT id
        FROM shu_users
        WHERE is_deleted = 0
        AND mobile IN (%s)
        """
        if mobile:
            command = command % ','.join(["'"+i+"'" for i in mobile])
        else:
            return []
        result = cursor.query(command)

        return [str(i['id']) for i in result] if result else []

    @staticmethod
    def get_new_users(cursor, params, promoter_ids=None):
        """用户拉新统计"""
        try:
            command = """
            SELECT FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d') AS create_time, COUNT(*) AS count
            FROM shu_recommended_users
            WHERE create_time >= :start_time
            AND create_time < :end_time
            AND is_deleted = 0
            %s
            GROUP BY FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d')"""

            # 城市经理且推广人员为空
            if params['role'] == 4 and not promoter_ids:
                command = command % 'AND referrer_user_id IN (0) '
            # 非城市经理查看所有人
            elif not promoter_ids:
                command = command % ''
            # 城市经理且有推广人员
            else:
                referrer_user_id = 'AND referrer_user_id IN (%s) ' % ','.join(promoter_ids)
                command = command % referrer_user_id

            promote_quality = cursor.query(command, {
                'start_time': params['start_time'],
                'end_time': params['end_time'],
            })
            # 累计
            before_promote_count = 0
            if params['data_type'] == 2:
                command = """
                SELECT COUNT(*) AS count
                FROM shu_recommended_users
                WHERE create_time < :start_time
                AND is_deleted = 0
                %s """

                # 城市经理且推广人员为空
                if params['role'] == 4 and not promoter_ids:
                    command = command % 'AND referrer_user_id IN (0) '
                # 非城市经理查看所有人
                elif not promoter_ids:
                    command = command % ''
                # 城市经理且有推广人员
                else:
                    referrer_user_id = 'AND referrer_user_id IN (%s) ' % ','.join(promoter_ids)
                    command = command % referrer_user_id

                before_promote = cursor.query_one(command, {
                    'start_time': params['start_time'],
                })
                before_promote_count = before_promote['count'] if before_promote else 0

            return promote_quality if promote_quality else [], before_promote_count

        except Exception as e:
            log.error('用户拉新统计异常: [error: %s]' % e)

    @staticmethod
    def get_user_behavior(cursor, params, promoter_ids=None):
        """用户行为统计"""
        try:
            # 登录
            if params.get('data_type') == 1:
                command = """
                -- 用户登录
                SELECT FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d') AS create_time, COUNT(*) AS count

                FROM shu_recommended_users
                LEFT JOIN shu_user_stats ON shu_recommended_users.recommended_user_id = shu_user_stats.user_id
                AND shu_user_stats.last_login_time > shu_recommended_users.create_time

                WHERE create_time >= :start_time
                AND create_time < :end_time
                AND is_deleted = 0
                %s
                GROUP BY FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d')
                """
            # 发货
            elif params.get('data_type') == 2:
                command = """ 
                -- 用户发货
                SELECT FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d') AS create_time, COUNT(*) AS count

                FROM shu_recommended_users

                WHERE create_time >= :start_time
                AND create_time < :end_time
                AND is_deleted = 0
                %s
                AND (SELECT COUNT(*)
                FROM shf_goods
                WHERE shf_goods.user_id = shu_recommended_users.recommended_user_id
                AND shf_goods.create_time > shu_recommended_users.create_time) > 0
                GROUP BY FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d')
                 """
            # 接单
            elif params.get('data_type') == 3:
                command = """
                -- 用户接单
                SELECT FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d') AS create_time, COUNT(*) AS count

                FROM shu_recommended_users

                WHERE create_time >= :start_time
                AND create_time < :end_time
                AND is_deleted = 0
                %s
                AND (SELECT COUNT(*)
                FROM shb_orders
                WHERE shb_orders.driver_id = shu_recommended_users.recommended_user_id
                AND shb_orders.create_time > shu_recommended_users.create_time) > 0
                GROUP BY FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d')
                 """
            # 完成订单
            elif params.get('data_type') == 4:
                command = """
                -- 用户完成订单
                SELECT FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d') AS create_time, COUNT(*) AS count

                FROM shu_recommended_users

                WHERE create_time >= :start_time
                AND create_time < :end_time
                AND is_deleted = 0
                %s
                AND (
                (SELECT COUNT(*)
                FROM shb_orders
                WHERE shb_orders.driver_id = shu_recommended_users.recommended_user_id
                AND shb_orders.create_time > shu_recommended_users.create_time
                AND shb_orders.`status` = 3) > 0
                OR
                (SELECT COUNT(*)
                FROM shb_orders
                WHERE shb_orders.owner_id = shu_recommended_users.recommended_user_id
                AND shb_orders.create_time > shu_recommended_users.create_time
                AND shb_orders.`status` = 3) > 0)
                GROUP BY FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d')
                """
            else:
                return []

            # 城市经理且推广人员为空
            if params['role'] == 4 and not promoter_ids:
                command = command % 'AND referrer_user_id IN (0) '
            # 非城市经理查看所有人
            elif not promoter_ids:
                command = command % ''
            # 城市经理且有推广人员
            else:
                referrer_user_id = 'AND referrer_user_id IN (%s) ' % ','.join(promoter_ids)
                command = command % referrer_user_id

            promote_quality = cursor.query(command, {
                'start_time': params['start_time'],
                'end_time': params['end_time'],
            })

            return promote_quality if promote_quality else []

        except Exception as e:
            log.error('用户行为统计异常: [error: %s]' % e)

    @staticmethod
    def get_money(cursor, params, promoter_ids=None):
        """用户金额统计"""
        try:
            # 货源总额
            if params.get('data_type') == 1:
                command = """
                -- 用户货源总额
                SELECT FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d') AS create_time, 
                SUM((SELECT SUM(price_expect + price_addition)
                FROM shf_goods
                WHERE shf_goods.user_id = shu_recommended_users.recommended_user_id
                AND shf_goods.create_time > shu_recommended_users.create_time)) AS count

                FROM shu_recommended_users

                WHERE create_time >= :start_time
                AND create_time < :end_time
                AND is_deleted = 0
                %s
                GROUP BY FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d')
                """
            # 订单总额
            elif params.get('data_type') == 2:
                command = """
                -- 用户订单总额
                SELECT FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d') AS create_time, 
                IF(SUM((SELECT SUM(price)
                FROM shb_orders
                WHERE shu_recommended_users.recommended_user_id = shb_orders.driver_id
                AND shb_orders.create_time > shu_recommended_users.create_time)) IS NULL, 0,
                SUM((SELECT SUM(price)
                FROM shb_orders
                WHERE shu_recommended_users.recommended_user_id = shb_orders.driver_id
                AND shb_orders.create_time > shu_recommended_users.create_time))) +
                IF(SUM((SELECT SUM(price)
                FROM shb_orders
                WHERE shu_recommended_users.recommended_user_id = shb_orders.owner_id
                AND shb_orders.create_time > shu_recommended_users.create_time)) IS NULL, 0,
                SUM((SELECT SUM(price)
                FROM shb_orders
                WHERE shu_recommended_users.recommended_user_id = shb_orders.owner_id
                AND shb_orders.create_time > shu_recommended_users.create_time))) AS count

                FROM shu_recommended_users

                WHERE create_time >= :start_time
                AND create_time < :end_time
                AND is_deleted = 0
                %s
                GROUP BY FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d')
                """
            # 实际完成总额
            elif params.get('data_type') == 3:
                command = """
                -- 用户订单完成总额
                SELECT FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d') AS create_time, 
                IF(SUM((SELECT SUM(price)
                FROM shb_orders
                WHERE shu_recommended_users.recommended_user_id = shb_orders.driver_id
                AND shb_orders.create_time > shu_recommended_users.create_time
                AND shb_orders.`status` = 3)) IS NULL, 0,
                SUM((SELECT SUM(price)
                FROM shb_orders
                WHERE shu_recommended_users.recommended_user_id = shb_orders.driver_id
                AND shb_orders.create_time > shu_recommended_users.create_time
                AND shb_orders.`status` = 3))) +
                IF(SUM((SELECT SUM(price)
                FROM shb_orders
                WHERE shu_recommended_users.recommended_user_id = shb_orders.owner_id
                AND shb_orders.create_time > shu_recommended_users.create_time
                AND shb_orders.`status` = 3)) IS NULL, 0,
                SUM((SELECT SUM(price)
                FROM shb_orders
                WHERE shu_recommended_users.recommended_user_id = shb_orders.owner_id
                AND shb_orders.create_time > shu_recommended_users.create_time
                AND shb_orders.`status` = 3))) AS count

                FROM shu_recommended_users

                WHERE create_time >= :start_time
                AND create_time < :end_time
                AND is_deleted = 0
                %s
                GROUP BY FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d')
                """
            else:
                return []

            # 城市经理且推广人员为空
            if params['role'] == 4 and not promoter_ids:
                command = command % 'AND referrer_user_id IN (0) '
            # 非城市经理查看所有人
            elif not promoter_ids:
                command = command % ''
            # 城市经理且有推广人员
            else:
                referrer_user_id = 'AND referrer_user_id IN (%s) ' % ','.join(promoter_ids)
                command = command % referrer_user_id

            promote_quality = cursor.query(command, {
                'start_time': params['start_time'],
                'end_time': params['end_time'],
            })

            for i in promote_quality:
                if not i['count']:
                    i['count'] = 0

            return promote_quality if promote_quality else []

        except Exception as e:
            log.error('用户金额统计异常: [error: %s]' % e)

