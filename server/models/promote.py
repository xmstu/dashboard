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
    def get_extension_worker_list(cursor, page, limit, params):
        try:
            fetch_where = ' AND 1 '
            command = """ 
                SELECT
                    reference_id,
                    reference_name,
                    reference_mobile
                FROM
                    tb_inf_promote
                where reference_id != 0 AND is_deleted = 0
                AND reference_id NOT IN (
                SELECT
                    tb_inf_user.reference_id 
                FROM
                    tb_inf_user
                    INNER JOIN tb_inf_promote ON tb_inf_user.reference_id = tb_inf_promote.reference_id 
                    AND tb_inf_user.is_deleted = 0 
                    AND tb_inf_promote.is_deleted = 0 
                ) 
                {fetch_where}
             """

            # 用户名
            if params['user_name']:
                fetch_where += """ AND tb_inf_promote.reference_name = '%s' """ % params['user_name']

            # 手机号
            if params['mobile']:
                fetch_where += """ AND tb_inf_promote.reference_mobile = %s """ % params['mobile']

            command = command.format(fetch_where=fetch_where)

            # 查询表的条数
            count_command = """
                        SELECT COUNT( * ) as promote_counts
                        FROM (%(command)s) as a
                        """

            promote_counts = cursor.query_one(count_command % {'command': command})

            # 分页
            command += """ LIMIT %s, %s """ % ((page - 1) * limit, limit)

            promote_effect_detail = cursor.query(command)

            extension_worker_list = {
                'promote_effect_detail': promote_effect_detail if promote_effect_detail else [],
                'count': promote_counts['promote_counts'] if promote_counts else 0
            }

            return extension_worker_list if extension_worker_list else None

        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数有误'))

    @staticmethod
    def get_promote_effect_list(cursor, page, limit, params):
        try:
            fetch_where = ' AND 1 '

            command = """
                    SELECT
                    tb_inf_user.reference_id,
                    reference_name,
                    reference_mobile,
                    -- 推荐人数
                    COUNT(*) AS user_count,
                    -- TODO 唤醒人数
                    0 AS wake_up_count,
                    -- 发货数
                    (SELECT COUNT(*) FROM tb_inf_goods 
                    WHERE
                        tb_inf_goods.user_id = tb_inf_user.user_id 
                        AND tb_inf_goods.create_time >= "%(start_time)s"
                        AND tb_inf_goods.create_time < "%(end_time)s"
                    ) AS goods_count,
                    -- 发货人数
                    (SELECT COUNT(DISTINCT user_id) FROM tb_inf_goods 
                    WHERE
                        tb_inf_goods.user_id = tb_inf_user.user_id 
                        AND tb_inf_goods.create_time >= "%(start_time)s" 
                        AND tb_inf_goods.create_time < "%(end_time)s"
                    ) AS goods_user_count,
                    -- 完成数
                    (SELECT SUM(order_count) FROM tb_inf_order 
                    WHERE
                        tb_inf_user.user_id = tb_inf_order.user_id 
                        AND tb_inf_order.`status` = 3 
                        AND tb_inf_order.create_time >= "%(start_time)s"
                        AND tb_inf_order.create_time < "%(end_time)s"
                    ) AS order_over_count,
                    -- 货源金额
                    (SELECT SUM(goods_price_sum) FROM tb_inf_goods 
                    WHERE
                        tb_inf_goods.user_id = tb_inf_user.user_id 
                        AND tb_inf_goods.create_time >= "%(start_time)s" 
                        AND tb_inf_goods.create_time < "%(end_time)s"
                    ) AS goods_price,
                    -- 完成金额
                    ( SELECT SUM(order_price_sum) FROM tb_inf_order 
                    WHERE
                        tb_inf_user.user_id = tb_inf_order.user_id 
                        AND tb_inf_order.`status` = 3 
                        AND tb_inf_order.create_time >= "%(start_time)s" 
                        AND tb_inf_order.create_time < "%(end_time)s"
                    ) AS order_over_price 
                FROM
                    tb_inf_user
                    INNER JOIN tb_inf_promote ON tb_inf_user.reference_id = tb_inf_promote.reference_id AND tb_inf_promote.is_deleted = 0
                    AND tb_inf_user.reference_id != 0 
                    LEFT JOIN tb_inf_goods ON tb_inf_user.user_id = tb_inf_goods.user_id 
                WHERE
                    -- 注册日期
                    tb_inf_user.create_time >= "%(start_time)s"
                    AND tb_inf_user.create_time < "%(end_time)s"
                    {fetch_where}
                    -- 名字
                    -- 手机号
                    -- 推荐角色
                    -- 货源类型
                    -- 是否活跃
                    -- 贴车贴
                GROUP BY
                    reference_id
            """

            # 用户名
            if params['user_name']:
                fetch_where += """ AND tb_inf_promote.reference_name = '%s' """ % params['user_name']

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
    command = """
    SELECT FROM_UNIXTIME(create_time, '%%Y-%%m-%%d'), COUNT(*) AS count
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


def get_user_behavior(cursor, params):
    if params.get('data_type') == 1:
        command = """
        -- 用户登录
        SELECT FROM_UNIXTIME(create_time, '%%Y-%%m-%%d'), COUNT(*) AS count
        
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
        SELECT FROM_UNIXTIME(create_time, '%%Y-%%m-%%d'), COUNT(*) AS count
        
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
        SELECT FROM_UNIXTIME(create_time, '%%Y-%%m-%%d'), COUNT(*) AS count
        
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
        SELECT FROM_UNIXTIME(create_time, '%%Y-%%m-%%d'), COUNT(*) AS count
        
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


def get_money(cursor, params):
    if params.get('data_type') == 1:
        command = """
        -- 用户货源总额
        SELECT FROM_UNIXTIME(create_time, '%%Y-%%m-%%d'), 
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
        SELECT FROM_UNIXTIME(create_time, '%%Y-%%m-%%d'), 
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
        SELECT FROM_UNIXTIME(create_time, '%%Y-%%m-%%d'), 
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
