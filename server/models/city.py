# -*- coding: utf-8 -*-

from server import log

class CityResourceBalanceModel(object):
    @staticmethod
    def get_goods_data(cursor, params):
        """获取货源数据"""
        command = '''
        SELECT shf_goods.id, shf_goods.`status`,
        -- 车型
        shf_goods_vehicles.`name` AS new_vehicle,
        -- 是否通话
        (SELECT COUNT(1)
        FROM shu_call_records
        WHERE source_type = 1
        AND source_id = shf_goods.id
        AND (owner_id = shf_goods.user_id OR user_id = shf_goods.user_id)) AS call_count
        
        FROM shf_goods
        LEFT JOIN shf_goods_vehicles ON shf_goods.id = shf_goods_vehicles.goods_id AND shf_goods_vehicles.vehicle_attribute = 3
        WHERE shf_goods.create_time >= :start_time
        AND shf_goods.create_time < :end_time
        -- 地区
        AND 1 = 1 %(region)s
        -- 货源类型
        AND 1 = 1 %(goods_type)s'''

        # 地区
        region = ''
        if params['region_id']:
            # 用户自选
            if isinstance(params['region_id'], int):
                region = 'AND (from_province_id = %(region_id)s OR from_city_id = %(region_id)s OR from_county_id = %(region_id)s OR from_town_id = %(region_id)s)' % {'region_id': params['region_id']}
            # 非管理员默认地区
            elif isinstance(params['region_id'], list):
                region = '''
                AND (
                from_province_id IN (%(region_id)s)
                OR from_city_id IN (%(region_id)s)
                OR from_county_id IN (%(region_id)s)
                OR from_town_id IN (%(region_id)s)
                )''' % {'region_id': ','.join(params['region_id'])}
        # 同城
        goods_type = ''
        if params['goods_type'] == 1:
            goods_type = 'AND haul_dist = 1'
        # 跨城定价
        elif params['goods_type'] == 2:
            goods_type = 'AND haul_dist = 2 AND goods_level = 2'
        # 跨城议价
        elif params['goods_type'] == 3:
            goods_type = 'AND haul_dist = 2 AND goods_level = 1'

        command = command % {
            'region': region,
            'goods_type': goods_type
        }
        result = cursor.query(command, {
            'start_time': params['start_time'],
            'end_time': params['end_time']
        })
        return result if result else []

    @staticmethod
    def get_booking_data(cursor, params):
        """获取线路车型"""
        command = """
        SELECT shf_booking_settings.user_id,
        IF(shf_booking_settings.vehicle_length_id = 0, '不限车型', shm_dictionary_items.`name`) AS booking_vehicle,
        orders.count
        FROM shf_booking_settings
        -- 同城、跨城
        %(goods_type)s
        LEFT JOIN shm_dictionary_items ON shf_booking_settings.vehicle_length_id = shm_dictionary_items.id
        LEFT JOIN (
        SELECT driver_id, COUNT(1) AS count
        FROM shb_orders
        WHERE create_time >= :start_time
        AND create_time < :end_time
        GROUP BY driver_id) AS orders ON shf_booking_settings.user_id = orders.driver_id
        
        WHERE shf_booking_settings.create_time >= :start_time
        AND shf_booking_settings.create_time < :end_time
        -- 地区
        AND 1 = 1 %(region)s"""

        # 地区
        region = ''
        if params['region_id']:
            # 用户字段
            if isinstance(params['region_id'], int):
                region = 'AND (from_province_id = %(region_id)s OR from_city_id = %(region_id)s OR from_county_id = %(region_id)s OR from_town_id = %(region_id)s)' % {'region_id': params['region_id']}
            # 非管理员默认地区
            elif isinstance(params['region_id'], list):
                region = '''
                AND (
                from_province_id IN (%(region_id)s)
                OR from_city_id IN (%(region_id)s)
                OR from_county_id IN (%(region_id)s)
                OR from_town_id IN (%(region_id)s)
                )''' % {'region_id': ','.join(params['region_id'])}
        # 同城
        if params['goods_type'] == 1:
            goods_type = 'INNER JOIN shf_booking_basis ON shf_booking_settings.user_id = shf_booking_basis.user_id AND enabled_short_haul = 1'
        # 跨城
        else:
            goods_type = 'INNER JOIN shf_booking_basis ON shf_booking_settings.user_id = shf_booking_basis.user_id AND enabled_long_haul = 1'
        command = command % {
            'region': region,
            'goods_type': goods_type
        }
        result = cursor.query(command, {
            'start_time': params['start_time'],
            'end_time': params['end_time']
        })
        return result if result else []

class CityOrderListModel(object):

    @staticmethod
    def get_data(cursor, page, limit, params):

        fields = """
            shf_goods.id,
            shf_goods.type,
            shf_goods.goods_level,
            shf_goods.haul_dist,
            shf_goods.`name`,
            shf_goods.weight,
            shf_goods.volume,
            shf_goods.from_province_id,
            shf_goods.from_city_id,
            shf_goods.from_county_id,
            shf_goods.from_town_id,
            shf_goods.from_address,
            shf_goods.to_province_id,
            shf_goods.to_city_id,
            shf_goods.to_county_id,
            shf_goods.to_town_id,
            shf_goods.to_address,
            shf_goods.mileage_total,
            -- 旧车型
            (SELECT IF(shf_goods_vehicles.attribute_value_id = 0, '不限车型', GROUP_CONCAT(shm_dictionary_items.`name`))
            FROM shf_goods_vehicles
            LEFT JOIN shm_dictionary_items ON shf_goods_vehicles.attribute_value_id = shm_dictionary_items.id AND shm_dictionary_items.is_deleted = 0
            WHERE shf_goods_vehicles.goods_id = shf_goods.id AND shf_goods_vehicles.vehicle_attribute = 1
            AND shf_goods_vehicles.is_deleted = 0
            ) AS vehicle_type,
            -- 新车型
            shf_goods_vehicles.`name` AS new_vehicle_type,
            shf_goods.price_recommend,
            shf_goods.price_expect,
            shf_goods.price_addition,
            shu_users.mobile,
            shu_user_profiles.user_name,
            -- 通话数
            (SELECT COUNT(1)
            FROM shu_call_records
            WHERE source_type = 1
            AND source_id = shf_goods.id
            AND (owner_id = shf_goods.user_id OR user_id = shf_goods.user_id)) AS call_count,
            shf_goods.create_time,
            FROM_UNIXTIME(shf_goods.create_time) AS shf_goods_create_time,
            -- 旧版装货时间
            shf_goods.loading_time_date,
            shf_goods.loading_time_period,
            -- 新版装货时间
            shf_goods.loading_time_period_end,
            FROM_UNIXTIME(shf_goods.loading_time_period_end) AS shf_goods_loading_time_period_end,
            -- 发货次数
            (SELECT COUNT(1) FROM shf_goods WHERE user_id = shu_users.id) AS goods_counts,
            shf_goods_vehicles.need_open_top,
            shf_goods_vehicles.need_tail_board,
            shf_goods_vehicles.need_flatbed,
            shf_goods_vehicles.need_high_sided,
            shf_goods_vehicles.need_box,
            shf_goods_vehicles.need_steel,
            shf_goods_vehicles.need_double_seat,
            shf_goods_vehicles.need_remove_seat
        """

        command = """
            SELECT
                %s 
            FROM shf_goods
            LEFT JOIN shu_user_profiles USING(user_id)
            LEFT JOIN shu_users ON shf_goods.user_id = shu_users.id 
            LEFT JOIN shf_goods_vehicles ON shf_goods_vehicles.goods_id = shf_goods.id
            AND shf_goods_vehicles.vehicle_attribute = 3 AND shf_goods_vehicles.is_deleted = 0
            WHERE shf_goods.expired_timestamp > UNIX_TIMESTAMP() 
            AND shf_goods.is_deleted = 0
            AND shf_goods.`status` IN (1, 2)
            {region}
        """

        # 地区
        region = ' AND 1=1 '
        if params['region_id']:
            # 用户自选
            if isinstance(params['region_id'], int):
                region = 'AND (from_province_id = %(region_id)s OR from_city_id = %(region_id)s OR from_county_id = %(region_id)s OR from_town_id = %(region_id)s) ' % {
                    'region_id': params['region_id']}
            # 非管理员默认地区
            elif isinstance(params['region_id'], list):
                region = '''
                        AND (
                        from_province_id IN (%(region_id)s)
                        OR from_city_id IN (%(region_id)s)
                        OR from_county_id IN (%(region_id)s)
                        OR from_town_id IN (%(region_id)s)
                        ) ''' % {'region_id': ','.join(params['region_id'])}

        command = command.format(region=region)

        # 货源类型
        if params['goods_type'] == 1:
            command += """ AND shf_goods.haul_dist = 1 AND shf_goods.type = 1 """
        elif params['goods_type'] == 2:
            command += """ AND shf_goods.haul_dist = 2 AND shf_goods.goods_level = 2 AND shf_goods.type = 1 """
        elif params['goods_type'] == 3:
            command += """ AND shf_goods.haul_dist = 2 AND shf_goods.goods_level = 1 AND shf_goods.type = 1 """
        elif params['goods_type'] == 4:
            command += """ AND shf_goods.type = 2 """

        # 车长
        if params['vehicle_length']:
            command += """ AND shf_goods_vehicles.name = '%s' """ % params['vehicle_length']

        # 是否通话
        if params.get('is_called'):
            called_sql = """ AND (SELECT COUNT(1)
                            FROM shu_call_records
                            WHERE source_type = 1
                            AND source_id = shf_goods.id
                            AND (owner_id = shf_goods.user_id OR user_id = shf_goods.user_id)) """
            if params['is_called'] == 1:
                command += called_sql + '> 0 '
            elif params['is_called'] == 2:
                command += called_sql + '= 0 '

        # 是否加价
        if params.get('is_addition'):
            if params['is_addition'] == 1:
                command += ' AND shf_goods.price_addition > 0 '
            elif params['is_addition'] == 2:
                command += ' AND shf_goods.price_addition = 0 '

        # 初次下单
        if params['spec_tag'] == 1:
            command += ' AND ( SELECT COUNT( 1 ) FROM shf_goods WHERE user_id = shu_users.id ) <= 3 '

        goods_counts = cursor.query_one(command % "COUNT(1) as goods_counts")

        command += ' ORDER BY shf_goods.id DESC LIMIT {0}, {1} '.format((page - 1) * limit, limit)

        goods_detail = cursor.query(command % fields)

        data = {
            'goods_detail': goods_detail if goods_detail else [],
            'goods_counts': goods_counts['goods_counts'] if goods_counts else 0,
        }

        return data


class CityNearbyCarsModel(object):

    @staticmethod
    def get_goods(cursor, goods_id):
        """货源"""
        command = '''SELECT
        from_province_id,
        from_city_id,
        from_county_id,
        from_town_id,
        to_province_id,
        to_city_id,
        to_county_id,
        to_town_id,
        from_longitude,
        from_latitude,
        shf_goods_vehicles.`name`,
        shf_goods_vehicles.inner_length,
        shf_goods.`status`
        FROM shf_goods
        LEFT JOIN shf_goods_vehicles ON shf_goods.id = shf_goods_vehicles.goods_id
        AND shf_goods_vehicles.vehicle_attribute = 3
        AND shf_goods_vehicles.is_deleted = 0
        WHERE shf_goods.id = :goods_id
        AND shf_goods.is_deleted = 0
        AND shf_goods.`status` IN (1, 2)'''

        goods = cursor.query_one(command, {
            'goods_id': goods_id
        })

        return goods if goods else {}



    @staticmethod
    def get_usual_region(cursor, from_city_id, from_county_id):
        """常驻地"""
        command = '''
        SELECT
        user_id,
        user_name,
        from_province_id,
        from_city_id,
        from_county_id,
        from_town_id,
        driver_auth AS auth_driver,
        mobile,
        order_count_SH + order_count_LH AS order_count,
        order_finished_count_SH_online + order_finished_count_SH_unline + order_finished_count_LH_online + order_finished_count_LH_unline AS order_finished,
        
        '常驻地' AS match_type
        
        FROM tb_inf_user
        WHERE from_city_id = :from_city_id AND from_county_id = :from_county_id
        AND last_login_time > UNIX_TIMESTAMP(DATE_SUB(CURDATE(),INTERVAL 2 DAY))
        AND driver_auth = 1
        LIMIT 10'''


        usual_regions = cursor.query(command, {
            'from_city_id': from_city_id,
            'from_county_id': from_county_id
        })

        return usual_regions if usual_regions else []

    @staticmethod
    def get_driver_info(cursor, ids):
        """获取司机信息"""
        try:
            command = """
            SELECT

            shu_user_profiles.user_id,
            (SELECT `name` FROM shm_dictionary_items WHERE id = shu_vehicle_auths.length_id) AS vehicle_length,
            (SELECT `name` FROM shm_dictionary_items WHERE id = shu_vehicle_auths.type_id) AS vehicle_type,
            shu_user_stats.credit_level,
            -- 诚信会员
            shu_user_profiles.is_trust_member,
            shu_user_profiles.trust_member_type,
            shu_user_profiles.ad_expired_time,
            0 AS inner_length,
            (SELECT COUNT(1) FROM shb_orders WHERE driver_id = shu_user_profiles.user_id) AS order_count,
            (SELECT COUNT(1) FROM shb_orders WHERE driver_id = shu_user_profiles.user_id AND shb_orders.`status` = 3) AS order_finished,
            (SELECT COUNT(1) FROM shb_orders WHERE driver_id = shu_user_profiles.user_id AND shb_orders.`status` = -1) AS order_cancel
            
            FROM shu_user_profiles
            INNER JOIN shu_user_stats ON shu_user_profiles.user_id = shu_user_stats.user_id
            LEFT JOIN shu_vehicles ON shu_vehicles.user_id = shu_user_profiles.user_id
            LEFT JOIN shu_vehicle_auths ON shu_vehicles.last_auth_id = shu_vehicle_auths.id AND shu_vehicle_auths.auth_status = 2 AND shu_vehicle_auths.is_deleted = 0
            
            WHERE shu_user_profiles.user_id IN (%s)
            GROUP BY shu_user_profiles.user_id
            """

            command = command % ','.join(ids)

            result = cursor.query(command)
            return result if result else []
        except Exception as e:
            log.error('获取司机信息出错: [error: %s]' % e, exc_info=True)



    @staticmethod
    def get_driver_by_booking(cursor, goods_id):
        """接单线路获取司机信息"""
        try:
            command = '''
            SELECT
            CASE WHEN 
                    (SELECT auth_driver FROM shu_user_auths
                     WHERE id = shu_user_profiles.last_auth_driver_id
                     AND auth_status = 2
                     AND is_deleted != 1) = 1
                    THEN 1 ELSE 0 END AS auth_driver,
            shf_booking_settings.user_id,
            shu_user_profiles.user_name,
            shu_users.mobile,
            (SELECT `name` FROM shm_dictionary_items WHERE id = shf_booking_settings.vehicle_length_id) AS vehicle_length,
            '' AS vehicle_type,
            shu_user_stats.credit_level,
            -- 诚信会员
            shu_user_profiles.is_trust_member,
            shu_user_profiles.trust_member_type,
            shu_user_profiles.ad_expired_time,
            0 AS inner_length,
            (SELECT COUNT(1) FROM shb_orders WHERE driver_id = shu_users.id) AS order_count,
            (SELECT COUNT(1) FROM shb_orders WHERE driver_id = shu_users.id AND shb_orders.`status` = 3) AS order_finished,
            (SELECT COUNT(1) FROM shb_orders WHERE driver_id = shu_users.id AND shb_orders.`status` = -1) AS order_cancel,
            '接单线路' AS match_type
            
            FROM shf_booking_settings, (
            SELECT
            from_county_id,
            from_town_id,
            to_county_id,
            to_town_id
            FROM shf_goods
            WHERE id = :goods_id AND is_deleted = 0
            ) AS goods, shu_user_profiles
            INNER JOIN shu_users ON shu_user_profiles.user_id = shu_users.id AND shu_users.is_deleted = 0
            INNER JOIN shu_user_stats ON shu_user_profiles.user_id = shu_user_stats.user_id
            
            WHERE
            shf_booking_settings.is_deleted = 0
            AND (
            -- 镇到镇
            (goods.from_town_id = shf_booking_settings.from_town_id
            AND goods.to_town_id = shf_booking_settings.to_town_id
            AND goods.from_town_id != 0
            AND goods.to_town_id != 0)
            -- 区到区
            OR (goods.from_county_id = shf_booking_settings.from_county_id
            AND goods.to_county_id = shf_booking_settings.to_county_id
            AND shf_booking_settings.from_town_id = 0
            AND shf_booking_settings.to_town_id = 0
            AND goods.from_county_id != 0
            AND goods.to_county_id != 0)
            -- 镇到区
            OR (goods.from_town_id = shf_booking_settings.from_town_id
            AND goods.to_county_id = shf_booking_settings.to_county_id
            AND shf_booking_settings.to_town_id = 0
            AND goods.from_town_id != 0
            AND goods.to_county_id != 0)
            -- 区到镇
            OR (goods.from_county_id = shf_booking_settings.from_county_id
            AND goods.to_town_id = shf_booking_settings.to_town_id
            AND shf_booking_settings.from_town_id = 0
            AND goods.from_county_id != 0
            AND goods.to_town_id != 0))
            AND shu_user_profiles.user_id = shf_booking_settings.user_id AND shu_user_profiles.is_deleted = 0 AND shu_user_profiles.`status` = 1
            AND shu_user_stats.last_login_time > UNIX_TIMESTAMP(DATE_SUB(CURDATE(),INTERVAL 1 DAY))
            LIMIT 30 '''

            driver_info = cursor.query(command, {
                'goods_id': goods_id
            })

            return driver_info if driver_info else []

        except Exception as e:
            log.error('接单线路获取司机信息出错: [error: %s]' % e, exc_info=True)