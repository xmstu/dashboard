# -*- coding: utf-8 -*-
import time

from flask_restful import abort

from server import log
from server.status import HTTPStatus, make_result, APIStatus


class PromoteEffectList(object):

    @staticmethod
    def check_extension_mobile(cursor, mobile):
        """检查推广人员id是否存在"""
        command = """SELECT id
        FROM shu_users
        WHERE mobile = :mobile
        AND is_deleted = 0
         """
        ret = cursor.query_one(command, {'mobile': mobile})

        return ret['id'] if ret else 0

    @staticmethod
    def check_promote_alive(cursor, promoter_id):
        """检查推广人员是否已存在"""
        command = """SELECT *
        FROM tb_inf_promote_rules
        WHERE promoter_id = :promoter_id AND promoter_status = 1 AND is_deleted = 0
         """
        ret = cursor.query_one(command, {'promoter_id': promoter_id})

        return ret if ret else {}

    @staticmethod
    def add_extension_worker(cursor, admin_id, promoter_id, admin_type):
        """新增推广人员"""
        command = """INSERT INTO tb_inf_promote_rules(admin_id, promoter_id, admin_type, create_time, update_time)
        VALUES (%s, %s, %s, %s, %s)"""
        try:
            result = cursor.insert(command, {
                'admin_id': admin_id,
                'promoter_id': promoter_id,
                'admin_type': admin_type,
                'create_time': int(time.time()),
                'update_time': int(time.time())
            })
            return result
        except Exception as e:
            log.error('新增推广人员异常[error: %s]' % (e))

    @staticmethod
    def delete_from_tb_inf_promte(cursor, admin_id, admin_type, promoter_id):
        """删除推广人员"""
        try:
            command = """UPDATE tb_inf_promote_rules
            SET promoter_status = 0
            WHERE admin_id = :admin_id AND promoter_id = :promoter_id"""
            row_count = cursor.update(command, {
                'admin_id': admin_id,
                'promoter_id': promoter_id
            })
            return row_count
        except Exception as e:
            log.error('删除推广人员异常[error: %s]' % (e))

    @staticmethod
    def get_extension_info(cursor, user_id):
        """获取城市经理手下"""
        promote_users = {}
        return [str(i['user_id']) for i in promote_users] if promote_users else []

    @staticmethod
    def get_extension_worker(cursor, page, limit, params, promoter=None):
        """获取推广人员"""
        try:
            fetch_where = ''
            command = """
            SELECT {select_fields}
            FROM tb_inf_user
            WHERE mobile IN (
            SELECT
            DISTINCT referrer_mobile
            FROM tb_inf_user
            WHERE referrer_mobile != ''
            ORDER BY user_id)
            {fetch_where}
            """

            # 用户名
            if params['user_name']:
                fetch_where += " AND user_name = '%s' " % params['user_name']

            # 手机号
            if params['mobile']:
                fetch_where += " AND mobile = '%s' " % params['mobile']

            # 城市经理筛选
            if promoter:
                fetch_where += ' AND user_id IN (%s) ' % ','.join(promoter)

            fetch_where += ' LIMIT %s, %s ' % ((page - 1) * limit, limit)

            count_sql = command.format(fetch_where=fetch_where, select_fields='COUNT(*) AS count')
            command = command.format(fetch_where=fetch_where, select_fields='user_id')

            count = cursor.query_one(count_sql)
            promote_users = cursor.query(command)

            promote = [str(i['user_id']) for i in promote_users] if promote_users else []
            count = count['count'] if count else 0

            return promote, count

        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数有误'))

    @staticmethod
    def get_promote_effect_list(cursor, page, limit, params):
        try:
            inner_where = ''
            fetch_where = ''

            command = """
            SELECT
            user_id,
            user_name,
            mobile,
            (SELECT COUNT(*) FROM tb_inf_user WHERE referrer_mobile = referrer.referrer_mobile) AS user_count,
            0 AS wake_up_count,
            (SELECT SUM(goods_count) FROM tb_inf_user WHERE referrer_mobile = referrer.referrer_mobile) AS goods_count,
            (SELECT COUNT(DISTINCT user_id) FROM tb_inf_user WHERE referrer_mobile = referrer.referrer_mobile AND goods_count != 0) AS goods_user_count,
            (SELECT SUM(order_finished_count) FROM tb_inf_user WHERE referrer_mobile = referrer.referrer_mobile) AS order_over_count,
            (SELECT SUM(goods_price) FROM tb_inf_user WHERE referrer_mobile = referrer.referrer_mobile) AS goods_price,
            (SELECT SUM(order_over_price) FROM tb_inf_user WHERE referrer_mobile = referrer.referrer_mobile) AS order_over_price
            
            FROM tb_inf_user
            -- 推荐人员
            INNER JOIN (
            SELECT
            DISTINCT referrer_mobile
            FROM tb_inf_user
            WHERE referrer_mobile != ''
            %(inner_where)s
            ORDER BY user_id
            LIMIT :page, :count) AS referrer ON tb_inf_user.mobile = referrer.referrer_mobile
            
            WHERE 1 = 1
            %(fetch_where)s
            ORDER BY user_id
            """

            # 用户名
            if params['user_name']:
                inner_where += """ AND user_name = '%s' """ % params['user_name']

            # 手机号
            if params['mobile']:
                fetch_where += """ AND tb_inf_promote.reference_mobile = %s """ % params['mobile']

            # 推荐角色
            if params['role_type']:
                fetch_where += """
                    AND (
                    (%(role_type)d = 0)
                    OR (%(role_type)d = 1 AND user_type = 1)
                    OR (%(role_type)d = 2 AND user_type = 2)
                    OR (%(role_type)d = 3 AND user_type = 3)
                    )
                """ % {"role_type": params['role_type']}

            # 货源类型
            if params['goods_type']:
                fetch_where += """ 
                    AND (
                    (%(goods_type)d = 0)
                    OR (%(goods_type)d = 1 AND haul_dist = 1)
                    OR (%(goods_type)d = 2 AND haul_dist = 2 AND goods_level = 2)
                    OR (%(goods_type)d = 3 AND haul_dist = 2 AND goods_level = 1)
                    OR (%(goods_type)d = 4 AND goods_type = 2)
                    )
                """ % {"goods_type": params["goods_type"]}

            # 是否活跃
            if params['is_actived']:

                fetch_where += """
                    AND (
                    (%(is_actived)d = 0)
                    OR (%(is_actived)d = 1 AND keep_login_days >= 7 AND last_login_time > UNIX_TIMESTAMP() - 1 * 86400)
                    OR (%(is_actived)d = 2 AND last_login_time < UNIX_TIMESTAMP() - 1 * 86400
                    AND last_login_time > UNIX_TIMESTAMP() - 3 * 86400)
                    OR (%(is_actived)d = 3 AND last_login_time < UNIX_TIMESTAMP() - 4 * 86400
                    AND last_login_time > UNIX_TIMESTAMP() - 10 * 86400)
                    OR (%(is_actived)d = 4 AND last_login_time < UNIX_TIMESTAMP() - 10 * 86400)
                    )
                """ % {"is_actived": params['is_actived']}

            # 贴车贴
            if params['is_car_sticker']:
                fetch_where += """
                    AND (
                    (%(is_car_sticker)d = 0)
                    OR (%(is_car_sticker)d = 1 AND is_advert = 1)
                    OR (%(is_car_sticker)d = 2 AND is_advert = 0)
                    )
                """ % {"is_car_sticker": params['is_car_sticker']}

            command = command.format(fetch_where=fetch_where)

            # 查询表的条数
            count_command = """
                    SELECT COUNT( * ) as promote_counts
                    FROM (%(command)s) as a
            """

            start_time = time.strftime('%Y-%m-%d', time.localtime(params['start_time'] or time.time() - 86400 * 7))
            end_time = time.strftime('%Y-%m-%d', time.localtime(params['end_time'] or time.time() - 86400))

            promote_counts = cursor.query_one(count_command % {'command': command % {"start_time": start_time, "end_time": end_time}})

            # 分页
            command += """ LIMIT %s, %s """ % ((page - 1) * limit, limit)

            promote_effect_detail = cursor.query(command % {"start_time": start_time, "end_time": end_time})

            promote_effect_list = {
                'promote_effect_detail': promote_effect_detail if promote_effect_detail else [],
                'count': promote_counts['promote_counts'] if promote_counts else 0
            }

            return promote_effect_list if promote_effect_list else None

        except Exception as e:
            log.error('获取推荐人员效果数据异常:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数有误'))


class PromoteQuality(object):

    @staticmethod
    def get_before_promote_count(cursor, params):
        command = """
            SELECT
                COUNT( * ) AS count 
            FROM
                tb_inf_user 
            -- 时间段
            WHERE
              create_time <= :start_time 
            -- 推荐人
            AND reference_id IS NOT NULL 
        """

        before_promote_count = cursor.query_one(command,
                            {'start_time': time.strftime('%Y-%m-%d', time.localtime(params['start_time']))}
                                                )

        return before_promote_count['count'] if before_promote_count else 0

def get_new_users(cursor, params):
    """用户拉新统计"""
    try:
        command = """
        SELECT FROM_UNIXTIME(create_time, '%%Y-%%m-%%d') AS create_time, COUNT(*) AS count
        FROM shu_recommended_users
        WHERE create_time >= :start_time
        AND create_time < :end_time
        AND is_deleted = 0
        GROUP BY FROM_UNIXTIME(create_time, '%%Y-%%m-%%d')"""

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
            AND is_deleted = 0"""

            before_promote = cursor.query_one(command, {
                'start_time': params['start_time'],
            })
            before_promote_count = before_promote['count'] if before_promote else 0

        return promote_quality if promote_quality else [], before_promote_count

    except Exception as e:
        log.error('用户拉新统计异常: [error: %s]' % e)


def get_user_behavior(cursor, params):
    try:
        if params.get('data_type') == 1:
            command = """
            -- 用户登录
            SELECT FROM_UNIXTIME(create_time, '%%Y-%%m-%%d') AS create_time, COUNT(*) AS count
            
            FROM shu_recommended_users
            LEFT JOIN shu_user_stats ON shu_recommended_users.recommended_user_id = shu_user_stats.user_id
            AND shu_user_stats.last_login_time > shu_recommended_users.create_time
            
            WHERE create_time >= :start_time
            AND create_time < :end_time
            AND is_deleted = 0
            GROUP BY FROM_UNIXTIME(create_time, '%%Y-%%m-%%d')
            """

        elif params.get('data_type') == 2:
            command = """ 
            -- 用户发货
            SELECT FROM_UNIXTIME(create_time, '%%Y-%%m-%%d') AS create_time, COUNT(*) AS count
            
            FROM shu_recommended_users
            
            WHERE create_time >= :start_time
            AND create_time < :end_time
            AND is_deleted = 0
            AND (SELECT COUNT(*)
            FROM shf_goods
            WHERE shf_goods.user_id = shu_recommended_users.recommended_user_id
            AND shf_goods.create_time > shu_recommended_users.create_time) > 0
            GROUP BY FROM_UNIXTIME(create_time, '%%Y-%%m-%%d')
             """

        elif params.get('data_type') == 3:
            command = """
            -- 用户接单
            SELECT FROM_UNIXTIME(create_time, '%%Y-%%m-%%d') AS create_time, COUNT(*) AS count
            
            FROM shu_recommended_users
            
            WHERE create_time >= :start_time
            AND create_time < :end_time
            AND is_deleted = 0
            AND (SELECT COUNT(*)
            FROM shb_orders
            WHERE shb_orders.driver_id = shu_recommended_users.recommended_user_id
            AND shb_orders.create_time > shu_recommended_users.create_time) > 0
            GROUP BY FROM_UNIXTIME(create_time, '%%Y-%%m-%%d')
             """

        elif params.get('data_type') == 4:
            command = """
            -- 用户完成订单
            SELECT FROM_UNIXTIME(create_time, '%%Y-%%m-%%d') AS create_time, COUNT(*) AS count
            
            FROM shu_recommended_users
            
            WHERE create_time >= :start_time
            AND create_time < :end_time
            AND is_deleted = 0
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
            GROUP BY FROM_UNIXTIME(create_time, '%%Y-%%m-%%d')
            """
        else:
            return []

        promote_quality = cursor.query(command, {
            'start_time': params['start_time'],
            'end_time': params['end_time'],
        })

        return promote_quality if promote_quality else []

    except Exception as e:
        log.error('用户行为统计异常: [error: %s]' % e)


def get_money(cursor, params):
    try:
        if params.get('data_type') == 1:
            command = """
            -- 用户货源总额
            SELECT FROM_UNIXTIME(create_time, '%%Y-%%m-%%d') AS create_time, 
            SUM((SELECT SUM(price_expect + price_addition)
            FROM shf_goods
            WHERE shf_goods.user_id = shu_recommended_users.recommended_user_id
            AND shf_goods.create_time > shu_recommended_users.create_time)) AS count
            
            FROM shu_recommended_users
            
            WHERE create_time >= :start_time
            AND create_time < :end_time
            AND is_deleted = 0
            
            GROUP BY FROM_UNIXTIME(create_time, '%%Y-%%m-%%d')
            """
        elif params.get('data_type') == 2:
            command = """
            -- 用户订单总额
            SELECT FROM_UNIXTIME(create_time, '%%Y-%%m-%%d') AS create_time, 
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
            
            GROUP BY FROM_UNIXTIME(create_time, '%%Y-%%m-%%d')
            """
        elif params.get('data_type') == 3:
            command = """
            -- 用户订单完成总额
            SELECT FROM_UNIXTIME(create_time, '%%Y-%%m-%%d') AS create_time, 
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
            
            GROUP BY FROM_UNIXTIME(create_time, '%%Y-%%m-%%d')
            """
        else:
            return []

        promote_quality = cursor.query(command, {
            'start_time': params['start_time'],
            'end_time': params['end_time'],
        })

        return promote_quality if promote_quality else []

    except Exception as e:
        log.error('金额统计异常: [error: %s]' % e)
