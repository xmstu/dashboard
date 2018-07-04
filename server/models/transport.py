

class TransportRadarModel(object):

    @staticmethod
    def get_data(cursor, params):

        goods_cmd = """
        SELECT
            shf_goods_vehicles.name,
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
            AND shf_goods_vehicles.name IN ('小面包车', '中面包车', '小货车', '4.2米', '6.8米', '7.6米', '9.6米', '13米', '17米', '17.5米')
            GROUP BY shf_goods_vehicles.NAME
        """

        vehicle_cmd = """
        SELECT
            shm_dictionary_items.name,
            COUNT( 1 ) vehicle_count
        FROM
            shu_vehicle_auths
            INNER JOIN shu_vehicles ON shu_vehicle_auths.vehicle_id = shu_vehicles.id 
            INNER JOIN shf_booking_settings ON shf_booking_settings.user_id = shu_vehicles.user_id
            INNER JOIN shf_booking_basis ON shf_booking_settings.user_id = shf_booking_basis.user_id
            INNER JOIN shm_dictionary_items ON shm_dictionary_items.id = shu_vehicle_auths.length_id 
            -- 	接单线路创建时间
            AND shf_booking_settings.create_time >=:start_time
            AND shf_booking_settings.create_time < :end_time
            AND shu_vehicle_auths.is_deleted = 0 AND shu_vehicle_auths.auth_status = 2 
        WHERE
            {vehicle_sql}
            AND shm_dictionary_items.`name` IN ('小面包车', '中面包车', '小货车', '4.2米', '6.8米', '7.6米', '9.6米', '13米', '17米', '17.5米')
            GROUP BY shm_dictionary_items.`name`
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
            AND shb_orders.create_time >= :start_time
            AND shb_orders.create_time < :end_time
        WHERE
            {order_sql}
            AND shf_goods_vehicles.name IN ('小面包车', '中面包车', '小货车', '4.2米', '6.8米', '7.6米', '9.6米', '13米', '17米', '17.5米')
            GROUP BY shf_goods_vehicles.name
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

        # 出发地
        if params.get('from_province_id'):
            goods_sql += """ AND from_province_id = %d """ % params.get('from_province_id')
            vehicle_sql += """ AND from_province_id = %d """ % params.get('from_province_id')
            order_sql += """ AND shb_orders.from_province_id = %d """ % params.get('from_province_id')

        if params.get('from_city_id'):
            goods_sql += """ AND from_city_id = %d """ % params.get('from_city_id')
            vehicle_sql += """ AND from_city_id = %d """ % params.get('from_city_id')
            order_sql += """ AND shb_orders.from_city_id = %d """ % params.get('from_city_id')

        if params.get('from_county_id'):
            goods_sql += """ AND from_county_id = %d """ % params.get('from_county_id')
            vehicle_sql += """ AND from_county_id = %d """ % params.get('from_county_id')
            order_sql += """ AND shb_orders.from_county_id = %d """ % params.get('from_county_id')

        if params.get('from_town_id'):
            goods_sql += """ AND from_town_id = %d """ % params.get('from_town_id')
            vehicle_sql += """ AND from_town_id = %d """ % params.get('from_town_id')
            order_sql += """ AND shb_orders.from_town_id = %d """ % params.get('from_town_id')

        # 目的地
        if params.get('to_province_id'):
            goods_sql += """ AND to_province_id = %d """ % params.get('to_province_id')
            vehicle_sql += """ AND to_province_id = %d """ % params.get('to_province_id')
            order_sql += """ AND shb_orders.to_province_id = %d """ % params.get('to_province_id')

        if params.get('to_city_id'):
            goods_sql += """ AND to_city_id = %d """ % params.get('to_city_id')
            vehicle_sql += """ AND to_city_id = %d """ % params.get('to_city_id')
            order_sql += """ AND shb_orders.to_city_id = %d """ % params.get('to_city_id')

        if params.get('to_county_id'):
            goods_sql += """ AND to_county_id = %d """ % params.get('to_county_id')
            vehicle_sql += """ AND to_county_id = %d """ % params.get('to_county_id')
            order_sql += """ AND shb_orders.to_county_id = %d """ % params.get('to_county_id')

        if params.get('to_town_id'):
            goods_sql += """ AND to_town_id = %d """ % params.get('to_town_id')
            vehicle_sql += """ AND to_town_id = %d """ % params.get('to_town_id')
            order_sql += """ AND shb_orders.to_town_id = %d """ % params.get('to_town_id')

        kwargs = {
            'start_time': params.get('start_time'),
            'end_time': params.get('end_time')
        }

        vehicle_name_list = ['小面包车', '中面包车', '小货车', '4.2米', '6.8米', '7.6米', '9.6米', '13米', '17米', '17.5米']

        goods_count = cursor.query(goods_cmd.format(goods_sql=goods_sql), kwargs)
        vehicle_count = cursor.query(vehicle_cmd.format(vehicle_sql=vehicle_sql), kwargs)
        order_count = cursor.query(order_cmd.format(order_sql=order_sql), kwargs)

        goods_dict = {}
        vehicles_dict = {}
        orders_dict ={}

        for i in goods_count:
            goods_dict[i.get('name')] = i.get('goods_count')

        for i in vehicle_count:
            vehicles_dict[i.get('name')] = i.get('vehicle_count')

        for i in order_count:
            orders_dict[i.get('name')] = i.get('order_count')

        goods_ret = []
        vehicles_ret = []
        orders_ret = []

        # 车型
        for i in vehicle_name_list:
            goods_ret.append(goods_dict.get(i, 0))
            vehicles_ret.append(vehicles_dict.get(i, 0))
            orders_ret.append(orders_dict.get(i, 0))

        data = {
            'vehicle_name_list': vehicle_name_list,
            'goods_ret': goods_ret,
            'vehicles_ret': vehicles_ret,
            'orders_ret': orders_ret
        }

        return data


class TransportListModel(object):

    @staticmethod
    def get_data(cursor, page, limit, params):

        fields = """"""

        which_table = """"""

        fetch_where = """"""

        command = """"""

        data = cursor.query(command)

        return data