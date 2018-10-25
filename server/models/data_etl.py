# -*- coding: utf-8 -*-

from server.logger import log
import time, pymysql
import warnings
warnings.filterwarnings("ignore")


class daUserModel(object):
    @staticmethod
    def is_update(cursor):
        """判断da库是否需要更新"""
        try:
            command = "SELECT FROM_UNIXTIME(MAX(statistics_date), '%Y-%m-%d') AS statistics_date FROM tb_inf_user"
            result = cursor.query_one(command)
            log.debug('判断数据是否需要更新, [now: %s][statistics_date: %s]' % (int(time.time()), result['statistics_date']))
            return result['statistics_date'] if result['statistics_date'] else None
        except Exception as e:
            log.error('判断da库是否需要更新异常: [error: %s]' % e, exc_info=True)

    @staticmethod
    def delete_user_table(cursor):
        """清空用户表"""
        try:
            cursor.delete("DELETE FROM tb_inf_user")
            cursor.delete("ALTER TABLE tb_inf_user AUTO_INCREMENT = 1")
            log.debug('清空tb_inf_user表')
        except Exception as e:
            log.error('清空表异常: [error: %s]' % e, exc_info=True)

    @staticmethod
    def insert_data(cursor, data):
        """写入数据"""
        try:
            command = '''
            INSERT INTO tb_inf_user(
            user_id,
            user_name,
            mobile,
            user_type,
            goods_auth,
            driver_auth,
            company_auth,
            goods_count_SH,
            goods_count_LH,
            order_count_SH,
            order_count_LH,
            order_finished_count_SH_online,
            order_finished_count_SH_unline,
            order_finished_count_LH_online,
            order_finished_count_LH_unline,
            goods_price_SH,
            goods_price_LH,
            order_price_SH,
            order_price_LH,
            order_over_price_SH_online,
            order_over_price_SH_unline,
            order_over_price_LH_online,
            order_over_price_LH_unline,
            download_channel,
            from_channel,
            from_province_id,
            from_city_id,
            from_county_id,
            from_town_id,
            referrer_mobile,
            last_login_time,
            keep_login_days,
            is_sticker,
            recommended_status,
            vehicle_length_id,
            create_time,
            statistics_date)
            VALUES (
            :user_id,
            :user_name,
            :mobile,
            :user_type,
            :goods_auth,
            :driver_auth,
            :company_auth,
            :goods_count_SH,
            :goods_count_LH,
            :order_count_SH,
            :order_count_LH,
            :order_finished_count_SH_online,
            :order_finished_count_SH_unline,
            :order_finished_count_LH_online,
            :order_finished_count_LH_unline,
            :goods_price_SH,
            :goods_price_LH,
            :order_price_SH,
            :order_price_LH,
            :order_over_price_SH_online,
            :order_over_price_SH_unline,
            :order_over_price_LH_online,
            :order_over_price_LH_unline,
            :download_channel,
            :from_channel,
            :from_province_id,
            :from_city_id,
            :from_county_id,
            :from_town_id,
            :referrer_mobile,
            :last_login_time,
            :keep_login_days,
            :is_sticker,
            :recommended_status,
            :vehicle_length_id,
            :create_time,
            :statistics_date
            )'''
            cursor.insert(command, data)
            log.debug('写入tb_inf_user表: [count: %s]' % len(data))
        except Exception as e:
            if not isinstance(e, pymysql.err.IntegrityError):
                log.error('写入数据异常: [error: %s]' % e, exc_info=True)

    @staticmethod
    def insert_transport_vehicles(cursor, data):
        """写入数据"""
        try:
            command = '''
            INSERT INTO tb_inf_transport_vehicles(
            user_id,
            from_province_id,
            from_city_id,
            from_county_id,
            from_town_id,
            to_province_id,
            to_city_id,
            to_county_id,
            to_town_id,
            vehicle_length_id,
            create_time,
            statistics_date)
            VALUES (
            :user_id,
            :from_province_id,
            :from_city_id,
            :from_county_id,
            :from_town_id,
            :to_province_id,
            :to_city_id,
            :to_county_id,
            :to_town_id,
            :vehicle_length_id,
            :create_time,
            :statistics_date
            )'''
            cursor.insert(command, data)
            log.debug('写入tb_transport_vehicles表: [count: %s]' % len(data))
        except Exception as e:
            if not isinstance(e, pymysql.err.IntegrityError):
                log.error('写入数据异常: [error: %s]' % e, exc_info=True)


class UserInfoModel(object):
    @staticmethod
    def get_user_count(cursor):
        """获取用户总数"""
        try:
            command = "SELECT COUNT(*) AS count FROM shu_users WHERE is_deleted = 0"
            user_count = cursor.query_one(command)
            log.debug('获取用户总数: %s' % user_count['count'] if user_count['count'] else 0)
            return user_count['count'] if user_count['count'] else 0
        except Exception as e:
            log.error('获取用户总数异常: [error: %s]' % e, exc_info=True)

    @staticmethod
    def get_user_detail(cursor, count):
        """获取用户详情"""
        try:
            command = '''
            SELECT

            shu_users.id AS user_id,
            shu_user_profiles.user_name,
            shu_users.mobile,
            shu_user_profiles.user_type,
            goods_auth.auth_goods AS goods_auth,
            driver_auth.auth_driver AS driver_auth,
            company_auth.auth_company AS company_auth,
            (SELECT mobile FROM shu_users WHERE id = shu_recommended_users.referrer_user_id) AS referrer_mobile,
            (SELECT COUNT(*) FROM shf_goods WHERE user_id = shu_users.id AND haul_dist = 1) AS goods_count_SH,
            (SELECT COUNT(*) FROM shf_goods WHERE user_id = shu_users.id AND haul_dist = 2) AS goods_count_LH,
            ((SELECT COUNT(*) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 1 WHERE driver_id = shu_users.id) +
             (SELECT COUNT(*) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 1 WHERE owner_id = shu_users.id)) AS order_count_SH,
            ((SELECT COUNT(*) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 2 WHERE driver_id = shu_users.id) +
             (SELECT COUNT(*) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 2 WHERE owner_id = shu_users.id)) AS order_count_LH,
            ((SELECT COUNT(*) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 1 WHERE driver_id = shu_users.id AND shb_orders.`status` = 3 AND shb_orders.pay_status = 2) +
             (SELECT COUNT(*) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 1 WHERE owner_id = shu_users.id AND shb_orders.`status` = 3 AND shb_orders.pay_status = 2)) AS order_finished_count_SH_online,
            ((SELECT COUNT(*) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 1 WHERE driver_id = shu_users.id AND shb_orders.`status` = 3 AND shb_orders.paid_offline = 1) +
             (SELECT COUNT(*) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 1 WHERE owner_id = shu_users.id AND shb_orders.`status` = 3 AND shb_orders.paid_offline = 1)) AS order_finished_count_SH_unline,
            ((SELECT COUNT(*) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 2 WHERE driver_id = shu_users.id AND shb_orders.`status` = 3 AND shb_orders.pay_status = 2) +
             (SELECT COUNT(*) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 2 WHERE owner_id = shu_users.id AND shb_orders.`status` = 3 AND shb_orders.pay_status = 2)) AS order_finished_count_LH_online,
            ((SELECT COUNT(*) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 2 WHERE driver_id = shu_users.id AND shb_orders.`status` = 3 AND shb_orders.paid_offline = 1) +
             (SELECT COUNT(*) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 2 WHERE owner_id = shu_users.id AND shb_orders.`status` = 3 AND shb_orders.paid_offline = 1)) AS order_finished_count_LH_unline,
            (SELECT SUM(price_expect + price_addition) FROM shf_goods WHERE user_id = shu_users.id AND haul_dist = 1) AS goods_price_SH,
            (SELECT SUM(price_expect + price_addition) FROM shf_goods WHERE user_id = shu_users.id AND haul_dist = 2) AS goods_price_LH,
            ((SELECT COALESCE(SUM(price), 0) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 1 WHERE driver_id = shu_users.id AND shb_orders.`status` = 3) +
             (SELECT COALESCE(SUM(price), 0) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 1 WHERE owner_id = shu_users.id AND shb_orders.`status` = 3)) AS order_price_SH,
            ((SELECT COALESCE(SUM(price), 0) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 2 WHERE driver_id = shu_users.id AND shb_orders.`status` = 3) +
             (SELECT COALESCE(SUM(price), 0) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 2 WHERE owner_id = shu_users.id AND shb_orders.`status` = 3)) AS order_price_LH,
            ((SELECT COALESCE(SUM(price), 0) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 1 WHERE driver_id = shu_users.id AND shb_orders.`status` = 3 AND shb_orders.pay_status = 2) +
             (SELECT COALESCE(SUM(price), 0) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 1 WHERE owner_id = shu_users.id AND shb_orders.`status` = 3 AND shb_orders.pay_status = 2)) AS order_over_price_SH_online,
            ((SELECT COALESCE(SUM(price), 0) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 1 WHERE driver_id = shu_users.id AND shb_orders.`status` = 3 AND shb_orders.paid_offline = 1) +
             (SELECT COALESCE(SUM(price), 0) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 1 WHERE owner_id = shu_users.id AND shb_orders.`status` = 3 AND shb_orders.paid_offline = 1)) AS order_over_price_SH_unline,
            ((SELECT COALESCE(SUM(price), 0) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 2 WHERE driver_id = shu_users.id AND shb_orders.`status` = 3 AND shb_orders.pay_status = 2) +
             (SELECT COALESCE(SUM(price), 0) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 2 WHERE owner_id = shu_users.id AND shb_orders.`status` = 3 AND shb_orders.pay_status = 2)) AS order_over_price_LH_online,
            ((SELECT COALESCE(SUM(price), 0) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 2 WHERE driver_id = shu_users.id AND shb_orders.`status` = 3 AND shb_orders.paid_offline = 1) +
             (SELECT COALESCE(SUM(price), 0) FROM shb_orders INNER JOIN shf_goods ON shb_orders.goods_id = shf_goods.id AND haul_dist = 2 WHERE owner_id = shu_users.id AND shb_orders.`status` = 3 AND shb_orders.paid_offline = 1)) AS order_over_price_LH_unline,
            shu_user_profiles.download_channel,
            shu_user_profiles.from_channel,
            shu_users.create_time,
            shu_user_stats.last_login_time,
            shu_user_stats.keep_login_days,
            IF(shu_user_profiles.trust_member_type = 2 AND ad_expired_time > UNIX_TIMESTAMP(), 1, 0) AS is_sticker,
            CONCAT_WS(',', (SELECT GROUP_CONCAT(DISTINCT shu_vehicle_auths.length_id)
            FROM shb_orders
            LEFT JOIN shu_vehicle_auths ON shb_orders.vehicle_id = shu_vehicle_auths.vehicle_id
            WHERE shb_orders.driver_id = shu_users.id),
            (SELECT GROUP_CONCAT(DISTINCT shf_booking_settings.vehicle_length_id)
            FROM shf_booking_settings
            INNER JOIN shm_dictionary_items ON shf_booking_settings.vehicle_length_id = shm_dictionary_items.id
            WHERE shf_booking_settings.user_id = shu_users.id
            AND vehicle_length_id != 0),
            (SELECT GROUP_CONCAT(DISTINCT shu_vehicle_auths.length_id)
            FROM shu_vehicles
            INNER JOIN shu_vehicle_auths ON shu_vehicles.id = shu_vehicle_auths.vehicle_id
            AND shu_vehicle_auths.is_deleted = 0 AND shu_vehicle_auths.auth_status = 2
            WHERE shu_vehicles.user_id = shu_users.id)) AS vehicle_length_id,
            (CASE shu_recommended_users.status 
            WHEN 0 THEN 1
            WHEN 1 THEN 2
            ELSE 0
            END
            ) recommended_status
            
            FROM (
            SELECT *
            FROM shu_users
            WHERE is_deleted = 0
            LIMIT 10000 OFFSET :count) AS shu_users
            INNER JOIN shu_user_profiles ON shu_users.id = shu_user_profiles.user_id
            INNER JOIN shu_user_stats ON shu_users.id = shu_user_stats.user_id
            LEFT JOIN shu_recommended_users ON shu_users.id = shu_recommended_users.recommended_user_id
            LEFT JOIN shu_user_auths AS goods_auth ON goods_auth.id = shu_user_profiles.last_auth_goods_id AND goods_auth.auth_status = 2 AND goods_auth.is_deleted = 0
            LEFT JOIN shu_user_auths AS driver_auth ON driver_auth.id = shu_user_profiles.last_auth_driver_id AND driver_auth.auth_status = 2 AND driver_auth.is_deleted = 0
            LEFT JOIN shu_user_auths AS company_auth ON company_auth.id = shu_user_profiles.last_auth_company_id AND company_auth.auth_status = 2 AND company_auth.is_deleted = 0
            '''

            result = cursor.query(command, {'count': count})
            log.debug('获取用户信息详情: [count: %s]' % count)
            return result
        except Exception as e:
            log.error('获取用户信息详情异常: [error: %s]' % e, exc_info=True)

    @staticmethod
    def geet_user_resident(cursor, count):
        """获取用户常驻地"""
        try:
            command = '''
            SELECT *
            FROM
            -- 认证车辆
            (SELECT
            id,
            GROUP_CONCAT(vehicles.home_station_province_id) AS vehicles_prov,
            GROUP_CONCAT(vehicles.home_station_city_id) AS vehicles_city,
            GROUP_CONCAT(vehicles.home_station_county_id) AS vehicles_county,
            GROUP_CONCAT(vehicles.home_station_town_id) AS vehicles_town
            
            FROM (
            SELECT
            users.id,
            shu_vehicle_auths.home_station_province_id,
            shu_vehicle_auths.home_station_city_id,
            shu_vehicle_auths.home_station_county_id,
            shu_vehicle_auths.home_station_town_id,
            CASE WHEN @user_num = user_id
            THEN @order_num := @order_num + 1
            ELSE @order_num := 1
            END AS rownum,
            @user_num := users.id
            FROM (
            SELECT id
            FROM shu_users
            WHERE is_deleted = 0
            LIMIT 10000 OFFSET :count
            ) AS users
            LEFT JOIN shu_vehicles ON shu_vehicles.user_id = users.id AND shu_vehicles.is_deleted = 0
            LEFT JOIN shu_vehicle_auths ON shu_vehicle_auths.vehicle_id = shu_vehicles.id
            AND shu_vehicle_auths.auth_status = 2 AND shu_vehicle_auths.is_deleted = 0
            ORDER BY shu_vehicles.id DESC) AS vehicles
            WHERE vehicles.rownum <= 80
            GROUP BY vehicles.id) AS vehicles
            -- 货源
            INNER JOIN (SELECT
            id,
            GROUP_CONCAT(goods.from_province_id) AS goods_prov,
            GROUP_CONCAT(goods.from_city_id) AS goods_city,
            GROUP_CONCAT(goods.from_county_id) AS goods_county,
            GROUP_CONCAT(goods.from_town_id) AS goods_town
            
            FROM (
            SELECT
            users.id,
            shf_goods.from_province_id,
            shf_goods.from_city_id,
            shf_goods.from_county_id,
            shf_goods.from_town_id,
            CASE WHEN @user_num = user_id
            THEN @order_num := @order_num + 1
            ELSE @order_num := 1
            END AS rownum,
            @user_num := users.id
            FROM (
            SELECT id
            FROM shu_users
            WHERE is_deleted = 0
            LIMIT 10000 OFFSET :count
            ) AS users
            LEFT JOIN shf_goods ON shf_goods.user_id = users.id
            ORDER BY shf_goods.id DESC) AS goods
            WHERE goods.rownum <= 80
            GROUP BY goods.id) AS goods USING(id)
            -- 订单
            INNER JOIN (SELECT
            id,
            GROUP_CONCAT(orders.from_province_id) AS order_prov,
            GROUP_CONCAT(orders.from_city_id) AS order_city,
            GROUP_CONCAT(orders.from_county_id) AS order_county,
            GROUP_CONCAT(orders.from_town_id) AS order_town
            
            FROM (
            SELECT
            users.id,
            shb_orders.from_province_id,
            shb_orders.from_city_id,
            shb_orders.from_county_id,
            shb_orders.from_town_id,
            CASE WHEN @user_num = driver_id
            THEN @order_num := @order_num + 1
            ELSE @order_num := 1
            END AS rownum,
            @user_num := users.id
            FROM (
            SELECT id
            FROM shu_users
            WHERE is_deleted = 0
            LIMIT 10000 OFFSET :count
            ) AS users
            LEFT JOIN shb_orders ON shb_orders.driver_id = users.id
            ORDER BY shb_orders.id DESC) AS orders
            WHERE orders.rownum <= 80
            GROUP BY orders.id) AS orders USING(id)
            -- 手机归属地
            INNER JOIN (
            SELECT
            users.id,
            IF(shu_user_profiles.mobile_area != '',
            (SELECT id FROM shm_regions WHERE `name` LIKE CONCAT('%%', SUBSTRING_INDEX(shu_user_profiles.mobile_area, ' ', -1), '%%') AND `level` = 2 AND is_deleted = 0 LIMIT 1),
            0) AS region_id
            FROM (
            SELECT id
            FROM shu_users
            WHERE is_deleted = 0
            LIMIT 10000 OFFSET :count
            ) AS users
            LEFT JOIN shu_user_profiles ON shu_user_profiles.user_id = users.id
            GROUP BY users.id
            ) AS mobile USING(id) '''
            # cursor.query('SET @order_num := 0')
            # cursor.query('SET @user_num := 0')
            result = cursor.query(command, {'count': count})
            log.debug('获取用户常驻地: [count: %s]' % count)
            return result

        except Exception as e:
            log.error('获取用户常驻地异常: [error: %s]' % e, exc_info=True)

    @staticmethod
    def get_last_login_user(cursor):
        """获取当天登录过用户"""
        try:
            command = '''SELECT user_id, last_login_time, keep_login_days, DATE_SUB(CURDATE(), INTERVAL 1 DAY) AS statistics_date
            FROM shu_user_stats
            WHERE last_login_time >= UNIX_TIMESTAMP(DATE_SUB(CURDATE(), INTERVAL 1 DAY))
            AND last_login_time < UNIX_TIMESTAMP(CURDATE())'''

            result = cursor.query(command)
            log.debug('获取当天登录过用户: [count: %s]' % len(result))
            return result if result else []

        except Exception as e:
            log.error('获取当天登录过用户异常: [error: %s]' % e, exc_info=True)

    @staticmethod
    def get_transport_vehicles(cursor, counts):
        """获取运力车型"""
        try:
            command = '''
            SELECT
            user_id,
            from_province_id,
            from_city_id,
            from_county_id,
            from_town_id,
            to_province_id,
            to_city_id,
            to_county_id,
            to_town_id,
            create_time,
            GROUP_CONCAT(vehicle_length_id) AS vehicle_length_id
            FROM (
            -- 接单线路
            SELECT
            user_id,
            from_province_id,
            from_city_id,
            from_county_id,
            from_town_id,
            to_province_id,
            to_city_id,
            to_county_id,
            to_town_id,
            FROM_UNIXTIME(shf_booking_settings.create_time, '%%Y-%%m-%%d') AS create_time,
            GROUP_CONCAT(DISTINCT shf_booking_settings.vehicle_length_id) AS vehicle_length_id
            FROM (
            SELECT *
            FROM shu_users
            WHERE is_deleted = 0
            LIMIT 10000 OFFSET :counts) AS shu_users
            INNER JOIN shf_booking_settings ON shu_users.id = shf_booking_settings.user_id
            INNER JOIN shm_dictionary_items ON shf_booking_settings.vehicle_length_id = shm_dictionary_items.id
            WHERE vehicle_length_id != 0
            AND shf_booking_settings.create_time >= UNIX_TIMESTAMP(DATE_SUB(CURDATE(),INTERVAL 1 DAY))
            AND shf_booking_settings.create_time < UNIX_TIMESTAMP(CURDATE())
            GROUP BY user_id, from_province_id, from_city_id, from_county_id, from_town_id, to_province_id, to_city_id, to_county_id, to_town_id, FROM_UNIXTIME(shf_booking_settings.create_time, '%%Y-%%m-%%d')
            UNION
            -- 订单线路
            SELECT
            driver_id,
            from_province_id,
            from_city_id,
            from_county_id,
            from_town_id,
            to_province_id,
            to_city_id,
            to_county_id,
            to_town_id,
            FROM_UNIXTIME(shb_orders.create_time, '%%Y-%%m-%%d') AS create_time,
            GROUP_CONCAT(DISTINCT shu_vehicle_auths.length_id) AS vehicle_length_id
            FROM (
            SELECT *
            FROM shu_users
            WHERE is_deleted = 0
            LIMIT 10000 OFFSET :counts) AS shu_users
            INNER JOIN shb_orders ON shu_users.id = shb_orders.driver_id
            LEFT JOIN shu_vehicle_auths ON shb_orders.vehicle_id = shu_vehicle_auths.vehicle_id
            WHERE shb_orders.driver_id AND shu_vehicle_auths.length_id
            AND shb_orders.create_time >= UNIX_TIMESTAMP(DATE_SUB(CURDATE(),INTERVAL 1 DAY))
            AND shb_orders.create_time < UNIX_TIMESTAMP(CURDATE())
            GROUP BY driver_id, from_province_id, from_city_id, from_county_id, from_town_id, to_province_id, to_city_id, to_county_id, to_town_id, FROM_UNIXTIME(shb_orders.create_time, '%%Y-%%m-%%d')
            ) AS all_data
            GROUP BY user_id, from_province_id, from_city_id, from_county_id, from_town_id, to_province_id, to_city_id, to_county_id, to_town_id, create_time
            ORDER BY create_time'''

            result = cursor.query(command, {
                'counts': counts
            })
            return result if result else []

        except Exception as e:
            log.error('获取运力车型异常: [error: %s]' % e, exc_info=True)

    @staticmethod
    def add_last_login_user(cursor, params):
        """记录当天登录过用户"""
        try:
            command = '''INSERT INTO tb_inf_user_login(user_id, last_login_time, keep_login_days, statistics_date)
            VALUES (:user_id, :last_login_time, :keep_login_days, :statistics_date)'''

            result = cursor.insert(command, params)
            log.debug('记录当天登录过用户')
            return result if result else 0

        except Exception as e:
            if not isinstance(e, pymysql.err.IntegrityError):
                log.error('记录当天登录过用户异常: [error: %s]' % e, exc_info=True)