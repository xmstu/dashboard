# -*- coding: utf-8 -*-
from server import log
import time

class UserList(object):
    @staticmethod
    def get_user_id_by_home_station(cursor, params):
        """常驻地或认证获取user_id"""
        command = '''SELECT
        user_id
        FROM tb_inf_user
        WHERE from_province_id = :home_station_province AND from_city_id = :home_station_city AND from_county_id = :home_station_county'''

        result = cursor.query(command, {
            'home_station_province': params['home_station_province'],
            'home_station_city': params['home_station_city'],
            'home_station_county': params['home_station_county'],
        })

        return [str(i['user_id']) for i in result if i] if result else []

    @staticmethod
    def get_user_list(cursor, page, limit, params, user_station=None):
        # 查询字段
        fields = '''
            shu_users.id,
            shu_user_profiles.user_name,
            shu_users.mobile,
            shu_user_profiles.user_type,
            -- 认证角色
            CASE WHEN 
                (SELECT auth_goods FROM shu_user_auths
                 WHERE id = shu_user_profiles.last_auth_goods_id
                 AND auth_status = 2
                 AND is_deleted != 1) = 1
                THEN 1 ELSE 0 END AS auth_goods,
            CASE WHEN 
                (SELECT auth_driver FROM shu_user_auths
                 WHERE id = shu_user_profiles.last_auth_driver_id
                 AND auth_status = 2
                 AND is_deleted != 1) = 1
                THEN 1 ELSE 0 END AS auth_driver,
            CASE WHEN 
                (SELECT auth_company FROM shu_user_auths
                 WHERE id = shu_user_profiles.last_auth_company_id
                 AND auth_status = 2
                 AND is_deleted != 1) = 1
                THEN 1 ELSE 0 END AS auth_company,
            -- 常驻地(暂定司机车辆认证地)
            (SELECT shm_regions.full_short_name
            FROM shu_vehicles, shu_vehicle_auths, shm_regions
            WHERE shu_vehicles.user_id = shu_users.id
            AND shu_vehicles.id = shu_vehicle_auths.vehicle_id
            AND auth_status = 2
            AND shu_vehicle_auths.home_station_county_id = shm_regions.`code`
            LIMIT 1) AS usual_city,
            -- 发货数
            (SELECT COUNT(1) FROM shf_goods WHERE shf_goods.user_id = shu_users.id) AS goods_count,
           -- 订单数
            (SELECT COUNT(1) FROM shb_orders WHERE shb_orders.owner_id = shu_users.id) +
            (SELECT COUNT(1) FROM shb_orders WHERE shb_orders.driver_id = shu_users.id) AS order_count,
            -- 订单完成
            (SELECT COUNT(1) FROM shb_orders WHERE shb_orders.owner_id = shu_users.id AND shb_orders.`status` = 3 AND (shb_orders.pay_status = 2 OR shb_orders.paid_offline = 1)) +
            (SELECT COUNT(1) FROM shb_orders WHERE shb_orders.driver_id = shu_users.id AND shb_orders.`status` = 3 AND (shb_orders.pay_status = 2 OR shb_orders.paid_offline = 1)) AS order_completed,
            -- 下载、注册渠道
            shu_user_profiles.download_channel,
            shu_user_profiles.from_channel,
            -- 最后登录
            FROM_UNIXTIME(shu_user_stats.last_login_time, '%Y-%m-%d') AS last_login_time,
            FROM_UNIXTIME(shu_users.create_time, '%Y-%m-%d') AS create_time'''

        command = """
            SELECT
            %s
            FROM shu_users
            INNER JOIN shu_user_profiles ON shu_users.id = shu_user_profiles.user_id
            INNER JOIN shu_user_stats ON shu_users.id = shu_user_stats.user_id
            -- 被推荐
            LEFT JOIN shu_recommended_users AS recommended_user ON shu_users.id = recommended_user.recommended_user_id

            WHERE shu_users.is_deleted = 0
            """

        # 用户名
        if params['user_name']:
            command += 'AND shu_user_profiles.user_name = "%s" ' % params['user_name']
        # 手机号
        if params['mobile']:
            command += 'AND shu_users.mobile = "%s" ' % params['mobile']
        # 推荐人手机
        if params['reference_mobile']:
            command += '''AND shu_users.id IN (SELECT recommended_user_id
            FROM shu_recommended_users
            WHERE referrer_user_id = (SELECT id FROM shu_users WHERE mobile = "%s"))''' % params['reference_mobile']
        # 下载渠道
        if params['download_ch']:
            command += 'AND shu_user_profiles.download_channel = "%s" ' % params['download_ch']
        # 注册渠道
        if params['from_channel']:
            command += 'AND shu_user_profiles.from_channel = "%s" ' % params['from_channel']
        # 推荐注册
        if params['is_referenced'] == 1:
            command += 'AND recommended_user.id IS NOT NULL '
        elif params['is_referenced'] == 2:
            command += 'AND recommended_user.id IS NULL '
        # 常驻地
        if user_station:
            command += 'AND shu_users.id IN (%s)' % user_station
        # 注册角色
        if params['role_type'] == 1:
            command += 'AND shu_user_profiles.user_type = 1 '
        elif params['role_type'] == 2:
            command += 'AND shu_user_profiles.user_type = 2 '
        elif params['role_type'] == 3:
            command += 'AND shu_user_profiles.user_type = 3 '
        # 认证角色
        if params['role_auth'] == 1:
            command += '''
            AND (SELECT COUNT(1) FROM shu_user_auths
            WHERE shu_user_auths.id = shu_user_profiles.last_auth_goods_id AND shu_user_auths.auth_status = 2
            AND shu_user_auths.is_deleted = 0 AND shu_user_auths.auth_goods = 1) > 0 '''
        elif params['role_auth'] == 2:
            command += '''
            AND (SELECT COUNT(1) FROM shu_user_auths
            WHERE shu_user_auths.id = shu_user_profiles.last_auth_driver_id AND shu_user_auths.auth_status = 2
            AND shu_user_auths.is_deleted = 0 AND shu_user_auths.auth_driver = 1) > 0 '''
        elif params['role_auth'] == 3:
            command += '''
            AND (SELECT COUNT(1) FROM shu_user_auths
            WHERE shu_user_auths.id = shu_user_profiles.last_auth_company_id AND shu_user_auths.auth_status = 2
            AND shu_user_auths.is_deleted = 0 AND shu_user_auths.auth_company = 1) > 0 '''
        # 是否活跃
        if params['is_actived'] == 1:
            command += 'AND shu_user_stats.keep_login_days >= 7 AND shu_user_stats.last_login_time > UNIX_TIMESTAMP() - 1 * 86400 '
        elif params['is_actived'] == 2:
            command += '''AND shu_user_stats.last_login_time < UNIX_TIMESTAMP() - 1 * 86400
            AND shu_user_stats.last_login_time > UNIX_TIMESTAMP() - 3 * 86400 '''
        elif params['is_actived'] == 3:
            command += '''AND shu_user_stats.last_login_time < UNIX_TIMESTAMP() - 4 * 86400
            AND shu_user_stats.last_login_time > UNIX_TIMESTAMP() - 10 * 86400 '''
        elif params['is_actived'] == 4:
            command += '''AND shu_user_stats.last_login_time < UNIX_TIMESTAMP() - 10 * 86400 '''

        # 操作过
        if params['is_used']:
            pass

        # if params['is_used'] == 1:
        #     command += 'AND (SELECT COUNT(1) FROM shf_goods WHERE shf_goods.user_id = shu_users.id) > 0 '
        # elif params['is_used'] == 2:
        #     command += 'AND (SELECT COUNT(1) FROM shb_orders WHERE shb_orders.owner_id = shu_users.id OR shb_orders.driver_id = shu_users.id) > 0 '
        # elif params['is_used'] == 3:
        #     command += 'AND (SELECT COUNT(1) FROM shb_orders WHERE (shb_orders.owner_id = shu_users.id OR shb_orders.driver_id = shu_users.id) AND shb_orders.`status` = 3 AND (shb_orders.pay_status = 2 OR shb_orders.paid_offline = 1)) > 0 '

        # 贴车贴
        if params['is_car_sticker'] == 1:
            command += 'AND shu_user_profiles.trust_member_type = 2 AND ad_expired_time > UNIX_TIMESTAMP() '
        elif params['is_car_sticker'] == 2:
            command += 'AND shu_user_profiles.trust_member_type != 2 '
        # 最后登录
        if params['last_login_start_time'] and params['last_login_end_time']:
            command += 'AND shu_user_stats.last_login_time >= %s AND shu_user_stats.last_login_time < %s ' % (
            params['last_login_start_time'], params['last_login_end_time'])
        # 注册日期
        if params['register_start_time'] and params['register_end_time']:
            command += 'AND shu_users.create_time >= %s AND shu_users.create_time < %s ' % (
                params['register_start_time'], params['register_end_time'])

        # 优化初次加载速度
        fields_value = list(filter(lambda x: x, [params[i] for i in params]))
        if not fields_value:
            user_count = cursor.query_one('SELECT COUNT(1) AS count FROM shu_users WHERE shu_users.is_deleted = 0')
        else:
            user_count = cursor.query_one(command % 'COUNT(1) AS count')

        # TODO 排序优化 分页
        command += """ ORDER BY shu_users.id DESC LIMIT %s, %s """ % ((page - 1) * limit, limit)
        # 详情
        user_detail = cursor.query(command % fields)

        user_list = {
            'user_detail': user_detail if user_detail else [],
            'user_count': user_count['count'] if user_count['count'] else 0
        }
        log.info('user_list:{}'.format(user_list))

        return user_list


class UserStatistic(object):

    # @staticmethod
    # def get_before_user_count(cursor, params):
    #     """累计用户"""
    #     command = """
    #     SELECT COUNT(*) AS count
    #     FROM tb_inf_user
    #     WHERE create_time < :start_time
    #     -- 角色
    #     AND ((:role_type = 0)
    #     OR (:role_type = 1 AND user_type = 1)
    #     OR (:role_type = 2 AND user_type = 2)
    #     OR (:role_type = 3 AND user_type = 3)
    #     )
    #     -- 认证
    #     AND ((:is_auth = 0)
    #     OR (:is_auth = 1 AND (goods_auth = 1 OR driver_auth = 1 OR company_auth = 1))
    #     OR (:is_auth = 2 AND goods_auth = 0 AND driver_auth = 0 AND company_auth = 0)
    #     )
    #     """
    #     before_user_count = cursor.query_one(command, {
    #         'start_time': time.strftime('%Y-%m-%d', time.localtime(params['start_time'])),
    #         'role_type': params['role_type'],
    #         'is_auth': params['is_auth']
    #     })
    #
    #     return before_user_count['count'] if before_user_count else 0

    # @staticmethod
    # def get_user_statistic(cursor, params):
    #     """用户新增"""
    #     command = """
    #     SELECT create_time, COUNT(*) AS count
    #     FROM tb_inf_user
    #     WHERE create_time >= :start_time
    #     AND create_time < :end_time
    #     -- 角色
    #     AND ((:role_type = 0)
    #     OR (:role_type = 1 AND user_type = 1)
    #     OR (:role_type = 2 AND user_type = 2)
    #     OR (:role_type = 3 AND user_type = 3)
    #     )
    #     -- 认证
    #     AND ((:is_auth = 0)
    #     OR (:is_auth = 1 AND (goods_auth = 1 OR driver_auth = 1 OR company_auth = 1))
    #     OR (:is_auth = 2 AND goods_auth = 0 AND driver_auth = 0 AND company_auth = 0)
    #     )
    #     GROUP BY create_time
    #     """
    #
    #     user_statistic = cursor.query(command, {
    #         'start_time': time.strftime('%Y-%m-%d', time.localtime(params['start_time'])),
    #         'end_time': time.strftime('%Y-%m-%d', time.localtime(params['end_time'])),
    #         'role_type': params['role_type'],
    #         'is_auth': params['is_auth']
    #     })
    #
    #     return user_statistic if user_statistic else []

    @staticmethod
    def get_before_user_count_by_mobile(cursor, params):
        """累计用户"""
        command = """
        SELECT COUNT(1) AS count
        FROM shu_users
        INNER JOIN shu_user_profiles ON shu_users.id = shu_user_profiles.user_id
        LEFT JOIN shu_user_auths AS goods_auth ON goods_auth.id = shu_user_profiles.last_auth_goods_id AND goods_auth.auth_status = 2 AND goods_auth.is_deleted = 0
        LEFT JOIN shu_user_auths AS driver_auth ON driver_auth.id = shu_user_profiles.last_auth_driver_id AND driver_auth.auth_status = 2 AND driver_auth.is_deleted = 0
        LEFT JOIN shu_user_auths AS company_auth ON company_auth.id = shu_user_profiles.last_auth_company_id AND company_auth.auth_status = 2 AND company_auth.is_deleted = 0
        
        WHERE shu_users.is_deleted = 0
        AND shu_users.create_time < :start_time
        -- 角色
        AND ((:role_type = 0)
        OR (:role_type = 1 AND shu_user_profiles.user_type = 1)
        OR (:role_type = 2 AND shu_user_profiles.user_type = 2)
        OR (:role_type = 3 AND shu_user_profiles.user_type = 3)
        )
        -- 认证
        AND ((:is_auth = 0)
        OR (:is_auth = 1 AND (goods_auth.auth_goods = 1 OR driver_auth.auth_driver = 1 OR company_auth.auth_company = 1))
        OR (:is_auth = 2 AND (goods_auth.auth_goods IS NULL AND driver_auth.auth_driver IS NULL AND company_auth.auth_company IS NULL))
        )
        %s
        """
        # 优化查询速度
        if not params['role_type'] and not params['region_id'] and not params['is_auth']:
            before_user_count = cursor.query_one('''
            SELECT COUNT(1) AS count
            FROM shu_users
            WHERE shu_users.is_deleted = 0 AND shu_users.create_time < :start_time
            ''', {'start_time': params['start_time']})
        else:
            region = ''
            if params['region_id']:
                region = 'AND SUBSTRING_INDEX(shu_user_profiles.mobile_area, " ", -1) IN (%s)' % ','.join(params['region_id'])

            command = command % region

            before_user_count = cursor.query_one(command, {
                'start_time': params['start_time'],
                'role_type': params['role_type'],
                'is_auth': params['is_auth']
            })

        return before_user_count['count'] if before_user_count else 0

    @staticmethod
    def get_user_statistic_by_mobile(cursor, params):
        """用户常驻地还没更新，先用手机号归属地应付一下"""
        command = """
        SELECT
        FROM_UNIXTIME(shu_users.create_time, '%%%%Y-%%%%m-%%%%d') AS create_time,
        COUNT(1) AS count
        
        FROM shu_users
        INNER JOIN shu_user_profiles ON shu_users.id = shu_user_profiles.user_id
        LEFT JOIN shu_user_auths AS goods_auth ON goods_auth.id = shu_user_profiles.last_auth_goods_id AND goods_auth.auth_status = 2 AND goods_auth.is_deleted = 0
        LEFT JOIN shu_user_auths AS driver_auth ON driver_auth.id = shu_user_profiles.last_auth_driver_id AND driver_auth.auth_status = 2 AND driver_auth.is_deleted = 0
        LEFT JOIN shu_user_auths AS company_auth ON company_auth.id = shu_user_profiles.last_auth_company_id AND company_auth.auth_status = 2 AND company_auth.is_deleted = 0
        
        WHERE shu_users.is_deleted = 0
        AND shu_users.create_time >= :start_time
        AND shu_users.create_time < :end_time
        -- 角色
        AND ((:role_type = 0)
        OR (:role_type = 1 AND shu_user_profiles.user_type = 1)
        OR (:role_type = 2 AND shu_user_profiles.user_type = 2)
        OR (:role_type = 3 AND shu_user_profiles.user_type = 3)
        )
        -- 认证
        AND ((:is_auth = 0)
        OR (:is_auth = 1 AND (goods_auth.auth_goods = 1 OR driver_auth.auth_driver = 1 OR company_auth.auth_company = 1))
        OR (:is_auth = 2 AND (goods_auth.auth_goods IS NULL AND driver_auth.auth_driver IS NULL AND company_auth.auth_company IS NULL))
        )
        %s
        GROUP BY FROM_UNIXTIME(shu_users.create_time, '%%%%Y-%%%%m-%%%%d')
        """
        region = ''
        if params['region_id']:
            if isinstance(params['region_id'], set):
                region = 'AND SUBSTRING_INDEX(shu_user_profiles.mobile_area, " ", -1) IN (%s)' %  ','.join(params['region_id'])
            elif isinstance(params['region_id'], str):
                region = 'AND SUBSTRING_INDEX(shu_user_profiles.mobile_area, " ", -1) = %s' % params['region_id']

        command = command % region

        user_statistic = cursor.query(command, {
            'start_time': params['start_time'],
            'end_time': params['end_time'],
            'role_type': params['role_type'],
            'is_auth': params['is_auth']
        })

        return user_statistic if user_statistic else []
