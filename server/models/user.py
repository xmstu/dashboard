# -*- coding: utf-8 -*-
from server import log


class UserQuery(object):

    @staticmethod
    def get_area(cursor, ):
        pass


class UserList(object):

    @staticmethod
    def get_user_list(cursor, params):
        user_name = params.get('user_name', '')
        mobile = params.get('mobile', '')
        reference_mobile = params.get('reference_mobile', '')
        download_channel = params.get('download_channel', '')
        from_channel = params.get('from_channel', '')

        is_referenced = params.get('is_referenced')
        home_station_id = params.get('home_station_id')
        role_type = params.get('role_type')
        role_auth = params.get('role_auth')
        is_actived = params.get('is_actived')
        is_used = params.get('is_used')
        is_car_sticker = params.get('is_car_sticker')
        pages = params.get('pages')
        limit = params.get('limit')

        last_login_start_time = params.get('last_login_start_time', '')
        last_login_end_time = params.get('last_login_end_time', '')

        register_start_time = params.get('register_start_time', '')
        register_end_time = params.get('register_end_time', '')

        command = """
                    SELECT
                        shu_user_profiles.user_name,
                        shu_users.mobile,
                        shu_user_profiles.user_type,-- 认证角色
                    CASE
                            
                            WHEN ( SELECT auth_goods FROM shu_user_auths WHERE id = shu_user_profiles.last_auth_goods_id AND auth_status = 2 AND is_deleted != 1 ) = 1 THEN
                        1 ELSE 0 
                    END AS auth_goods,
                    CASE
                            
                            WHEN ( SELECT auth_driver FROM shu_user_auths WHERE id = shu_user_profiles.last_auth_driver_id AND auth_status = 2 AND is_deleted != 1 ) = 1 THEN
                            1 ELSE 0 
                        END AS auth_driver,
                    CASE
                            
                            WHEN ( SELECT auth_company FROM shu_user_auths WHERE id = shu_user_profiles.last_auth_company_id AND auth_status = 2 AND is_deleted != 1 ) = 1 THEN
                            1 ELSE 0 
                        END AS auth_company,-- 常驻地(暂定司机车辆认证地)
                        (
                        SELECT
                            shm_regions.full_short_name 
                        FROM
                            shu_vehicles,
                            shu_vehicle_auths,
                            shm_regions 
                        WHERE
                            shu_vehicles.user_id = shu_users.id 
                            AND shu_vehicles.id = shu_vehicle_auths.vehicle_id 
                            AND auth_status = 2 
                            AND shu_vehicle_auths.home_station_county_id = shm_regions.`code` 
                            LIMIT 1 
                        ) AS usual_city,-- 发货数
                        ( SELECT COUNT( * ) FROM shf_goods WHERE shf_goods.user_id = shu_users.id ) AS goods_count,-- 订单数
                        ( SELECT COUNT( * ) FROM shb_orders WHERE shb_orders.owner_id = shb_orders.id OR shb_orders.driver_id = shb_orders.id ) AS order_count,-- 订单完成
                        (
                        SELECT
                            COUNT( * ) 
                        FROM
                            shb_orders 
                        WHERE
                            ( shb_orders.owner_id = shb_orders.id OR shb_orders.driver_id = shb_orders.id ) 
                            AND shb_orders.`status` = 3 
                        ) AS order_completed,-- 下载、注册渠道
                        shu_user_profiles.download_channel,
                        shu_user_profiles.from_channel,-- 最后登录
                        FROM_UNIXTIME( shu_user_stats.last_login_time, '%Y-%m-%d' ) AS last_login_time,
                        FROM_UNIXTIME( shu_users.create_time, '%Y-%m-%d' ) AS create_time 
                    FROM
                        shu_users
                        LEFT JOIN shu_user_profiles ON shu_users.id = shu_user_profiles.user_id
                        LEFT JOIN shu_user_stats ON shu_users.id = shu_user_stats.user_id
                        LEFT JOIN shu_user_auths ON shu_users.id = shu_user_auths.user_id 
                    WHERE
                        shu_users.is_deleted = 0 
                    -- 用户名
                    -- AND shu_user_profiles.user_name = :user_name
                    -- 手机号
                    -- AND shu_users.mobile = :mobile
                    -- 推荐人手机
                    -- AND shu_user_profiles.reference_id = (SELECT id FROM shu_users WHERE mobile = :mobile)
                    -- 下载渠道
                    -- AND shu_user_profiles.download_channel = :download_channel
                    -- 注册渠道
                    -- AND shu_user_profiles.from_channel = :from_channel
                    -- 认证角色(货主、司机、物流公司)
                    -- AND shu_user_auths.auth_goods = 1 AND shu_user_auths.auth_status = 2 AND shu_user_auths.is_deleted = 0
                    -- AND shu_user_auths.auth_driver = 1 AND shu_user_auths.auth_status = 2 AND shu_user_auths.is_deleted = 0
                    -- AND shu_user_auths.auth_company = 1 AND shu_user_auths.auth_status = 2 AND shu_user_auths.is_deleted = 0
                    -- 是否活跃(待定)
                    -- 操作过(货源、订单、完成订单)
                    -- HAVING goods_count > 0
                    -- HAVING order_count > 0
                    -- HAVING order_completed > 0
                    -- 贴车贴
                    -- AND shu_user_profiles.trust_member_type = 2 AND ad_expired_time > UNIX_TIMESTAMP()
                    -- 分页
                        
                """

        if user_name:
            command += 'AND shu_user_profiles.user_name = "%s" ' % user_name

        if mobile:
            command += 'AND shu_users.mobile = %s ' % mobile

        if reference_mobile:
            command += 'AND shu_user_profiles.reference_id = (SELECT id FROM shu_users WHERE mobile = %s)' % mobile

        if download_channel:
            command += 'AND shu_user_profiles.download_channel = %s' % download_channel

        if from_channel:
            command += 'AND shu_user_profiles.from_channel = %s' % from_channel

        command += """
                    ORDER BY
                    shu_user_stats.last_login_time DESC 
                    LIMIT 0,
                    11
                    """

        user_list = cursor.query(command)

        log.info("获取sql参数:{}".format(params))
        log.info("获取user_list{}".format(user_list))
        return user_list if user_list else None
