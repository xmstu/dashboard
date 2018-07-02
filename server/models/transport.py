

class TransportRadarModel(object):

    @staticmethod
    def get_data(cursor, params):

        goods_cmd = """
        SELECT
            COUNT( 1 ) goods_count
        FROM
            shf_goods
            LEFT JOIN shf_goods_vehicles ON shf_goods_vehicles.goods_id = shf_goods.id 
            AND shf_goods_vehicles.vehicle_attribute = 3 
            AND shf_goods_vehicles.is_deleted = 0 
            AND shf_goods.create_time >= :start_time 
            AND shf_goods.create_time < :end_time
        WHERE
            {goods_sql}
        """

        vehicle_cmd = """
        SELECT
            COUNT( 1 ) vehicle_count
        FROM
            shf_booking_settings -- 在时间段内有登录过的用户
            INNER JOIN shu_user_stats ON shf_booking_settings.user_id = shu_user_stats.user_id 
            INNER JOIN shf_booking_basis ON shf_booking_settings.user_id = shf_booking_basis.user_id
            INNER JOIN shm_dictionary_items ON shf_booking_basis.short_haul_vehicle_length_id = shm_dictionary_items.id
            AND shu_user_stats.last_login_time >= :start_time 
            AND shu_user_stats.last_login_time < :end_time  
            AND shf_booking_settings.is_deleted = 0 
        WHERE
            {vehicle_sql}
        """

        order_cmd = """
        SELECT
            COUNT( 1 ) order_count
        FROM
            shb_orders INNER JOIN shf_goods ON shf_goods.id = shb_orders.goods_id
            LEFT JOIN shf_goods_vehicles ON shf_goods_vehicles.goods_id = shb_orders.goods_id 
            AND shf_goods_vehicles.vehicle_attribute = 3 
            AND shf_goods_vehicles.is_deleted = 0 
            AND shb_orders.create_time >= :start_time
            AND shb_orders.create_time < :end_time
        WHERE
            {order_sql}
        """

        goods_sql = """ 1=1 """
        vehicle_sql = """ 1=1 """
        order_sql = """ 1=1 """

        # 地区
        region = ' AND 1=1 '
        order_region = ' AND 1=1 '
        if params['region_id']:
            if isinstance(params['region_id'], int):
                region = ' AND (from_province_id = %(region_id)s OR from_city_id = %(region_id)s OR from_county_id = %(region_id)s OR from_town_id = %(region_id)s) ' % {'region_id': params['region_id']}
                order_region = ' AND (shb_orders.from_province_id = %(region_id)s OR shb_orders.from_city_id = %(region_id)s OR shb_orders.from_county_id = %(region_id)s OR shb_orders.from_town_id = %(region_id)s) ' % {'region_id': params['region_id']}
            elif isinstance(params['region_id'], list):
                region = '''
                        AND (
                        from_province_id IN (%(region_id)s)
                        OR from_city_id IN (%(region_id)s)
                        OR from_county_id IN (%(region_id)s)
                        OR from_town_id IN (%(region_id)s)
                        ) ''' % {'region_id': ','.join(params['region_id'])}
                order_region = '''
                        AND (
                        shb_orders.from_province_id IN (%(region_id)s)
                        OR shb_orders.from_city_id IN (%(region_id)s)
                        OR shb_orders.from_county_id IN (%(region_id)s)
                        OR shb_orders.from_town_id IN (%(region_id)s)
                        ) ''' % {'region_id': ','.join(params['region_id'])}

        goods_sql += region
        vehicle_sql += region
        order_sql += order_region

        # 同城/跨城
        if params.get('business'):
            goods_sql += """
            AND
            (
            ( {0}=1 AND haul_dist = 1) OR
            ( {0}=2 AND haul_dist = 2)
            )
            """.format(params['business'])

            vehicle_sql += """
            AND
            (
            ( {0}=1 AND shf_booking_basis.enabled_long_haul = 1) OR
            ( {0}=2 AND shf_booking_basis.enabled_short_haul = 1)
            )
            """.format(params['business'])

            order_sql += """ 
            AND 
            (
            ( {0}=1 AND shf_goods.haul_dist = 1 ) OR
            ( {0}=2 AND shf_goods.haul_dist = 2 )
            )
            """.format(params['business'])

        kwargs = {
            'start_time': params.get('start_time'),
            'end_time': params.get('end_time')
        }

        vehicle_name_list = ['小面包车', '中面包车', '小货车', '4.2米', '6.8米', '7.6米', '9.6米', '13米', '17米']

        # 车型
        goods_ret = []
        vehicles_ret = []
        orders_ret = []

        goods_sql += """ AND shf_goods_vehicles.NAME = '%s' """
        vehicle_sql += """ AND shm_dictionary_items.`name` = '%s' """
        order_sql += """ AND shf_goods_vehicles.NAME = '%s' """

        for i in vehicle_name_list:
            goods_count = cursor.query_one(goods_cmd.format(goods_sql=goods_sql % i), kwargs)['goods_count']
            vehicle_count = cursor.query_one(vehicle_cmd.format(vehicle_sql=vehicle_sql % i), kwargs)['vehicle_count']
            order_count = cursor.query_one(order_cmd.format(order_sql=order_sql % i), kwargs)['order_count']

            goods_ret.append(goods_count if goods_count else 0)
            vehicles_ret.append(vehicle_count if vehicle_count else 0)
            orders_ret.append(order_count if order_count else 0)

        data = {
            'vehicle_name_list': vehicle_name_list,
            'goods_ret': goods_ret,
            'vehicles_ret': vehicles_ret,
            'orders_ret': orders_ret
        }

        return data
