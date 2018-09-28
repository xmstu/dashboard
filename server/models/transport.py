from server import log
from server.cache_data import vehicle_id_list, init_regions
from server.utils.constant import vehicle_name_id, vehicle_name_list


class TransportRadarModel(object):

    @staticmethod
    def get_data(cursor1, cursor2, params):

        goods_cmd = """
        SELECT
            shf_goods_vehicles.name,
            COUNT( 1 ) goods_count
        FROM
            shf_goods
            LEFT JOIN shf_goods_vehicles ON shf_goods_vehicles.goods_id = shf_goods.id 
            AND shf_goods_vehicles.vehicle_attribute = 3 
            AND shf_goods_vehicles.is_deleted = 0 
        WHERE
            {goods_sql}
            AND shf_goods.is_deleted = 0
            AND shf_goods_vehicles.name IN ('小面包车', '中面包车', '小货车', '4.2米', '5.2米', '6.8米', '7.6米', '9.6米', '13米', '17.5米')
            AND shf_goods.create_time >= :start_time 
            AND shf_goods.create_time < :end_time
            GROUP BY shf_goods_vehicles.NAME
        """

        vehicle_cmd = """
        SELECT
            {vehicle_count} vehicle_count
        FROM
            `tb_inf_transport_vehicles` vehicle
            LEFT JOIN tb_inf_user user USING(user_id)
            WHERE
            {vehicle_sql}
            AND UNIX_TIMESTAMP(vehicle.create_time) < :end_time
            AND vehicle.vehicle_length_id != ''
            AND vehicle.vehicle_length_id REGEXP ",{vehicle_id}|{vehicle_id},|,{vehicle_id},|^{vehicle_id}$"
        """

        order_cmd = """
        SELECT
            shf_goods_vehicles.name,
            COUNT( 1 ) order_count
        FROM
            shb_orders INNER JOIN shf_goods ON shf_goods.id = shb_orders.goods_id
            LEFT JOIN shf_goods_vehicles ON shf_goods_vehicles.goods_id = shb_orders.goods_id 
            AND shf_goods_vehicles.vehicle_attribute = 3 
            AND shf_goods_vehicles.is_deleted = 0 
        WHERE
            {order_sql}
            AND shb_orders.is_deleted = 0 AND shb_orders.`status` != -1
            AND shf_goods_vehicles.name IN ('小面包车', '中面包车', '小货车', '4.2米', '5.2米', '6.8米', '7.6米', '9.6米', '13米', '17.5米')
            AND shb_orders.create_time >= :start_time
            AND shb_orders.create_time < :end_time
            GROUP BY shf_goods_vehicles.name
        """

        goods_sql = """ 1=1 """
        vehicle_sql = """ 1=1 """
        order_sql = """ 1=1 """

        # 地区
        goods_region = ' AND 1=1 '
        vehicle_region = ' AND 1=1 '
        order_region = ' AND 1=1 '
        if params['region_id']:
            if isinstance(params['region_id'], int):
                goods_region = ' AND (from_province_id = %(region_id)s OR from_city_id = %(region_id)s OR from_county_id = %(region_id)s OR from_town_id = %(region_id)s) ' % {'region_id': params['region_id']}
                vehicle_region = ' AND (vehicle.from_province_id = %(region_id)s OR vehicle.from_city_id = %(region_id)s OR vehicle.from_county_id = %(region_id)s OR vehicle.from_town_id = %(region_id)s) ' % {'region_id': params['region_id']}
                order_region = ' AND (shb_orders.from_province_id = %(region_id)s OR shb_orders.from_city_id = %(region_id)s OR shb_orders.from_county_id = %(region_id)s OR shb_orders.from_town_id = %(region_id)s) ' % {'region_id': params['region_id']}
            elif isinstance(params['region_id'], list):
                goods_region = '''
                        AND (
                        from_province_id IN (%(region_id)s)
                        OR from_city_id IN (%(region_id)s)
                        OR from_county_id IN (%(region_id)s)
                        OR from_town_id IN (%(region_id)s)
                        ) ''' % {'region_id': ','.join(params['region_id'])}
                vehicle_region = '''
                        AND (
                        vehicle.from_province_id IN (%(region_id)s)
                        OR vehicle.from_city_id IN (%(region_id)s)
                        OR vehicle.from_county_id IN (%(region_id)s)
                        OR vehicle.from_town_id IN (%(region_id)s)
                        ) ''' % {'region_id': ','.join(params['region_id'])}

                order_region = '''
                        AND (
                        shb_orders.from_province_id IN (%(region_id)s)
                        OR shb_orders.from_city_id IN (%(region_id)s)
                        OR shb_orders.from_county_id IN (%(region_id)s)
                        OR shb_orders.from_town_id IN (%(region_id)s)
                        ) ''' % {'region_id': ','.join(params['region_id'])}

        goods_sql += goods_region
        vehicle_sql += vehicle_region
        order_sql += order_region

        # # 同城/跨城/零担
        # if params.get('business'):
        #     goods_sql += """
        #     AND
        #     (
        #     ( {0}=1 AND haul_dist = 1) OR
        #     ( {0}=2 AND haul_dist = 2) OR
        #     ( {0}=3 AND type = 2)
        #     )
        #     """.format(params['business'])
        #
        #     order_sql += """
        #     AND
        #     (
        #     ( {0}=1 AND shf_goods.haul_dist = 1 ) OR
        #     ( {0}=2 AND shf_goods.haul_dist = 2 ) OR
        #     ( {0}=2 AND shf_goods.type = 2 )
        #     )
        #     """.format(params['business'])
        #
        # # 议价/一口价
        # if params.get('business_price'):
        #     goods_sql += """
        #                 AND
        #                 (
        #                 ( {0}=1 AND goods_level = 1) OR
        #                 ( {0}=2 AND is_system_price = 1)
        #                 )
        #                 """.format(params['business_price'])
        #
        #     order_sql += """
        #                 AND
        #                 (
        #                 ( {0}=1 AND shf_goods.goods_level = 1 ) OR
        #                 ( {0}=2 AND shf_goods.is_system_price = 1 )
        #                 )
        #                 """.format(params['business_price'])

        # 出发地
        if params.get('from_province_id'):
            goods_sql += """ AND from_province_id = %d """ % params.get('from_province_id')
            vehicle_sql += """ AND vehicle.from_province_id = %d """ % params.get('from_province_id')
            order_sql += """ AND shb_orders.from_province_id = %d """ % params.get('from_province_id')

        if params.get('from_city_id'):
            goods_sql += """ AND from_city_id = %d """ % params.get('from_city_id')
            vehicle_sql += """ AND vehicle.from_city_id = %d """ % params.get('from_city_id')
            order_sql += """ AND shb_orders.from_city_id = %d """ % params.get('from_city_id')

        if params.get('from_county_id'):
            goods_sql += """ AND from_county_id = %d """ % params.get('from_county_id')
            vehicle_sql += """ AND vehicle.from_county_id = %d """ % params.get('from_county_id')
            order_sql += """ AND shb_orders.from_county_id = %d """ % params.get('from_county_id')

        if params.get('from_town_id'):
            goods_sql += """ AND from_town_id = %d """ % params.get('from_town_id')
            vehicle_sql += """ AND vehicle.from_town_id = %d """ % params.get('from_town_id')
            order_sql += """ AND shb_orders.from_town_id = %d """ % params.get('from_town_id')

        # 目的地
        if params.get('to_province_id'):
            goods_sql += """ AND to_province_id = %d """ % params.get('to_province_id')
            vehicle_sql += """ AND vehicle.to_province_id = %d """ % params.get('to_province_id')
            order_sql += """ AND shb_orders.to_province_id = %d """ % params.get('to_province_id')

        if params.get('to_city_id'):
            goods_sql += """ AND to_city_id = %d """ % params.get('to_city_id')
            vehicle_sql += """ AND vehicle.to_city_id = %d """ % params.get('to_city_id')
            order_sql += """ AND shb_orders.to_city_id = %d """ % params.get('to_city_id')

        if params.get('to_county_id'):
            goods_sql += """ AND to_county_id = %d """ % params.get('to_county_id')
            vehicle_sql += """ AND vehicle.to_county_id = %d """ % params.get('to_county_id')
            order_sql += """ AND shb_orders.to_county_id = %d """ % params.get('to_county_id')

        if params.get('to_town_id'):
            goods_sql += """ AND to_town_id = %d """ % params.get('to_town_id')
            vehicle_sql += """ AND vehicle.to_town_id = %d """ % params.get('to_town_id')
            order_sql += """ AND shb_orders.to_town_id = %d """ % params.get('to_town_id')

        kwargs = {
            'start_time': params.get('start_time'),
            'end_time': params.get('end_time')
        }

        # 活跃车辆数
        vehicles_ret = []
        # 累计车辆数(非活跃和活跃)
        vehicles_all_ret = []
        vehicle_sql1 = vehicle_sql + """ AND UNIX_TIMESTAMP(vehicle.create_time) >= :start_time AND user.last_login_time >= :start_time AND user.last_login_time < :end_time """
        for i in vehicle_id_list:
            try:
                vehicle_all_count = cursor2.query_one(vehicle_cmd.format(vehicle_count="COUNT( DISTINCT user_id )", vehicle_sql=vehicle_sql, vehicle_id=i), kwargs)
                vehicles_all_ret.append(vehicle_all_count['vehicle_count'])

                vehicle_count = cursor2.query_one(vehicle_cmd.format(vehicle_count="COUNT(1)", vehicle_sql=vehicle_sql1, vehicle_id=i), kwargs)
                vehicles_ret.append(vehicle_count['vehicle_count'])

            except Exception as e:
                log.error('Error:{}'.format(e))
                vehicles_ret.append(0)

        goods_count = cursor1.query(goods_cmd.format(goods_sql=goods_sql), kwargs)
        order_count = cursor1.query(order_cmd.format(order_sql=order_sql), kwargs)

        goods_dict = {i.get('name'): i.get('goods_count') for i in goods_count}
        orders_dict = {i.get('name'): i.get('order_count') for i in order_count}

        goods_ret = []
        orders_ret = []

        # 车型
        for i in vehicle_name_list:
            goods_ret.append(goods_dict.get(i, 0))
            orders_ret.append(orders_dict.get(i, 0))

        data = {
            'vehicle_name_list': vehicle_name_list,
            'goods_ret': goods_ret,
            'vehicles_ret': vehicles_ret,
            'vehicles_all_ret': vehicles_all_ret,
            'orders_ret': orders_ret
        }

        return data


class TransportListModel(object):

    @staticmethod
    def get_data(cursor, params):

        fields = """
        from_province_id,
        from_city_id,
        from_county_id,
        to_province_id,
        to_city_id,
        to_county_id,
        COUNT( 1 ) AS vehicle_count,
        IFNULL(
        (
        SELECT
            COUNT( DISTINCT shu_vehicles.user_id ) 
        FROM
            shf_booking_settings AS sbs
            INNER JOIN shu_user_stats ON shu_user_stats.user_id = sbs.user_id 
        WHERE
            sbs.id = shf_booking_settings.id 
            AND shu_user_stats.last_login_time >= :start_time
            AND shu_user_stats.last_login_time < :end_time
        ) , 0) AS login_driver_count,
        COUNT( DISTINCT shu_vehicles.user_id ) AS total_driver_count 
        """

        fetch_where = """
        AND 1=1
        """

        command = """
        SELECT
            {fields}
        FROM
            shf_booking_settings
            INNER JOIN shu_vehicles ON shf_booking_settings.user_id = shu_vehicles.user_id
            INNER JOIN shu_vehicle_auths ON shu_vehicle_auths.vehicle_id = shu_vehicles.id 
            AND shu_vehicles.is_deleted = 0 
            AND shu_vehicle_auths.auth_status = 2 
            AND shu_vehicle_auths.is_deleted = 0
        WHERE
            shf_booking_settings.is_deleted = 0 
            AND from_city_id = :from_city_id 
            AND to_city_id = :to_city_id 
            AND shf_booking_settings.create_time >= :start_time
            AND shf_booking_settings.create_time < :end_time
            {fetch_where}
        GROUP BY
            from_city_id,
            to_city_id
        """
        # 地区权限
        region = ' AND 1=1 '
        if params['region_id'] and isinstance(params['region_id'], list):
            region = '''
                    AND (
                    shf_booking_settings.from_province_id IN (%(region_id)s)
                    OR shf_booking_settings.from_city_id IN (%(region_id)s)
                    OR shf_booking_settings.from_county_id IN (%(region_id)s)
                    OR shf_booking_settings.from_town_id IN (%(region_id)s)
                    ) ''' % {'region_id': ','.join(params['region_id'])}

        fetch_where += region

        # 是否计算区镇
        if params["calc_town"]:
            fetch_where += """
            AND (
            ({calc_town}=1 AND from_county_id != 0) OR
            ({calc_town}=2 AND to_county_id != 0)
            )
            """.format(calc_town=params["calc_town"])

        count = cursor.query(command.format(fields="COUNT(1) AS count", fetch_where=fetch_where), params)
        count = len(count)

        command += " LIMIT {0}, {1}".format(params["page"], params["limit"])

        transport_list = cursor.query(command.format(fields=fields, fetch_where=fetch_where), params)

        return {"count": count if count else 0, "transport_list": transport_list if transport_list else []}
