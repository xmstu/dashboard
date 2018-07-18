from server import log
from server.utils.constant import vehicle_name_id


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
            AND shf_goods_vehicles.name IN ('小面包车', '中面包车', '小货车', '4.2米', '6.8米', '7.6米', '9.6米', '13米', '17.5米')
            AND shf_goods.create_time >= :start_time 
            AND shf_goods.create_time < :end_time
            GROUP BY shf_goods_vehicles.NAME
        """

        vehicle_cmd = """
        SELECT
            COUNT(1) vehicle_count
        FROM
            `tb_inf_transport_vehicles` vehicle
            LEFT JOIN tb_inf_user user USING(user_id)
            WHERE
            {vehicle_sql}
            AND user.last_login_time >= :start_time 
            AND user.last_login_time < :end_time
            AND vehicle.create_time >= FROM_UNIXTIME(:start_time)
            AND vehicle.create_time < FROM_UNIXTIME(:end_time)
            AND vehicle.vehicle_length_id != ''
            AND vehicle.vehicle_length_id LIKE "%%{vehicle_id}%%"
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
            AND shf_goods_vehicles.name IN ('小面包车', '中面包车', '小货车', '4.2米', '6.8米', '7.6米', '9.6米', '13米', '17.5米')
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

        # 同城/跨城
        if params.get('business'):
            goods_sql += """
            AND
            (
            ( {0}=1 AND haul_dist = 1) OR
            ( {0}=2 AND haul_dist = 2)
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

        vehicle_name_list = ['小面包车', '中面包车', '小货车', '4.2米', '6.8米', '7.6米', '9.6米', '13米', '17.5米']
        vehicle_id_list = ['118', '119', '274', '18', '20', '21', '23', '31', '25']

        # 获取每种常用车型的数量
        vehicles_ret = []
        for i in vehicle_id_list:
            try:
                vehicle_count = cursor2.query_one(vehicle_cmd.format(vehicle_sql=vehicle_sql, vehicle_id=i), kwargs)
                if vehicle_count:
                    vehicles_ret.append(vehicle_count['vehicle_count'])
                else:
                    vehicles_ret.append(0)
            except Exception as e:
                log.error('Error:{}'.format(e))
                vehicles_ret.append(0)

        goods_count = cursor1.query(goods_cmd.format(goods_sql=goods_sql), kwargs)
        order_count = cursor1.query(order_cmd.format(order_sql=order_sql), kwargs)

        goods_dict = {}
        orders_dict ={}

        for i in goods_count:
            goods_dict[i.get('name')] = i.get('goods_count')

        for i in order_count:
            orders_dict[i.get('name')] = i.get('order_count')

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
            'orders_ret': orders_ret
        }

        return data


class TransportListModel(object):

    @staticmethod
    def get_data(cursor1, cursor2, page, limit, params):

        filelds = """
            FROM_UNIXTIME(sg.create_time, "%%Y-%%m-%%d") as create_time,
            haul_dist,
            sg.from_province_id,
            sg.from_city_id,
            sg.from_county_id,
            sg.to_province_id,
            sg.to_city_id,
            sg.to_county_id,
            AVG(mileage_total) AS avg_mileage_total,
            COUNT( 1 ) AS goods_count,
            COUNT(so.id) AS order_count
        """

        inner_good_order_fetch_where = """ 1=1 """
        inner_vehicle_fetch_where = """ 1=1 """

        cmd1 = """ 
            -- 货源和订单查询
        SELECT
            {filelds}
        FROM
            shf_goods sg
            LEFT JOIN shb_orders so ON sg.id = so.goods_id
            LEFT JOIN shf_goods_vehicles ON shf_goods_vehicles.goods_id = sg.id 
            AND shf_goods_vehicles.vehicle_attribute = 3 
            AND shf_goods_vehicles.is_deleted = 0 
        WHERE
            {inner_good_order_fetch_where}
            AND sg.is_deleted = 0 AND so.is_deleted = 0 AND so.`status` != -1
            -- 时间
            AND sg.create_time >= :start_time 
            AND sg.create_time < :end_time
            GROUP BY 
            sg.from_province_id,
            sg.from_city_id,
            sg.from_county_id,
            sg.to_province_id,
            sg.to_city_id,
            sg.to_county_id
        """

        cmd2 = """
        SELECT
            vehicle.from_province_id,
            vehicle.from_city_id,
            vehicle.from_county_id,
            vehicle.to_province_id,
            vehicle.to_city_id,
            vehicle.to_county_id,
            COUNT(1) vehicle_count
        FROM
            `tb_inf_transport_vehicles` vehicle
            LEFT JOIN tb_inf_user user USING(user_id)
            WHERE
            {inner_vehicle_fetch_where}
            AND user.last_login_time >= :start_time 
            AND user.last_login_time < :end_time
            AND vehicle.create_time >= FROM_UNIXTIME(:start_time)
            AND vehicle.create_time < FROM_UNIXTIME(:end_time)
            AND vehicle.vehicle_length_id != ''
            GROUP BY
            vehicle.from_province_id,
            vehicle.from_city_id,
            vehicle.from_county_id,
            vehicle.to_province_id,
            vehicle.to_city_id,
            vehicle.to_county_id;
        """

        # 地区权限
        region = ' AND 1=1 '
        if params['region_id']:
            if isinstance(params['region_id'], int):
                region = 'AND (from_province_id = %(region_id)s OR from_city_id = %(region_id)s OR from_county_id = %(region_id)s OR from_town_id = %(region_id)s) ' % {
                    'region_id': params['region_id']}
            elif isinstance(params['region_id'], list):
                region = '''
                        AND (
                        from_province_id IN (%(region_id)s)
                        OR from_city_id IN (%(region_id)s)
                        OR from_county_id IN (%(region_id)s)
                        OR from_town_id IN (%(region_id)s)
                        ) ''' % {'region_id': ','.join(params['region_id'])}

        inner_good_order_fetch_where += region
        inner_vehicle_fetch_where += region

        # 出发地
        if params['from_county_id']:
            inner_good_order_fetch_where += ' AND sg.from_county_id = %d ' % params['from_county_id']
            inner_vehicle_fetch_where += ' AND vehicle.from_county_id = %d ' % params['from_county_id']
        if params['from_city_id']:
            inner_good_order_fetch_where += ' AND sg.from_city_id = %d ' % params['from_city_id']
            inner_vehicle_fetch_where += ' AND vehicle.from_city_id = %d ' % params['from_city_id']
        if params['from_province_id']:
            inner_good_order_fetch_where += ' AND sg.from_province_id = %d ' % params['from_province_id']
            inner_vehicle_fetch_where += ' AND vehicle.from_province_id = %d ' % params['from_province_id']

        # 目的地
        if params['to_county_id']:
            inner_good_order_fetch_where += ' AND sg.to_county_id = %d ' % params['to_county_id']
            inner_vehicle_fetch_where += ' AND vehicle.to_county_id = %d ' % params['to_county_id']
        if params['to_city_id']:
            inner_good_order_fetch_where += ' AND sg.to_city_id = %d ' % params['to_city_id']
            inner_vehicle_fetch_where += ' AND vehicle.to_city_id = %d ' % params['to_city_id']
        if params['to_province_id']:
            inner_good_order_fetch_where += ' AND sg.to_province_id = %d ' % params['to_province_id']
            inner_vehicle_fetch_where += ' AND vehicle.to_province_id = %d ' % params['to_province_id']

        # 车长要求
        if params['vehicle_length']:
            inner_good_order_fetch_where += """ AND shf_goods_vehicles.`name` = '%s' """ % params['vehicle_length']
            inner_vehicle_fetch_where += """ AND vehicle.vehicle_length_id LIKE "%%{vehicle_id}%%" """.format(vehicle_id=vehicle_name_id.get(params['vehicle_length'], '小面包车'))

        # 业务类型
        if params['business']:
            inner_good_order_fetch_where += """ AND (({business}=1 AND haul_dist = 1) OR ({business}=2 AND haul_dist = 2)) """.format(business=params['business'])
            # inner_vehicle_fetch_where += """ AND (({business}=1 AND shf_booking_basis.enabled_long_haul = 1) OR ({business}=2 AND shf_booking_basis.enabled_short_haul = 1)) """.format(business=params['business'])

        # # 筛选条件
        # if params['filter']:
        #     outer_fetch_where += """ AND (({filter}=1 AND a.goods_count > IFNULL( b.vehicle_count, 0 )) OR ({filter}=2 AND a.goods_count < b.vehicle_count)) """.format(filter=params['filter'])

        # 时间
        kwargs = {
            'start_time': params.get('start_time', 0),
            'end_time': params.get('end_time', 0)
        }

        ret = cursor1.query(cmd1.format(filelds=""" COUNT(1) AS count """, inner_good_order_fetch_where=inner_good_order_fetch_where), kwargs)
        count = len(ret)

        cmd1 += """ ORDER BY create_time DESC LIMIT %s, %s """ % ((page - 1) * limit, limit)

        transport_list = cursor1.query(cmd1.format(filelds=filelds, inner_good_order_fetch_where=inner_good_order_fetch_where), kwargs)
        vehicle_list = cursor2.query(cmd2.format(inner_vehicle_fetch_where=inner_vehicle_fetch_where), kwargs)
        for i in transport_list:
            vehicle_count = [j['vehicle_count'] for j in vehicle_list if
                             i['from_province_id'] == j['from_province_id'] and i['from_city_id'] == j['from_city_id'] and i['from_county_id'] == j['from_county_id']
                             and i['to_province_id'] == j['to_province_id'] and i['to_city_id'] == j['to_city_id'] and i['to_county_id'] == j['to_county_id']
                             ]
            if vehicle_count:
                i['vehicle_count'] = vehicle_count[0]
            else:
                i['vehicle_count'] = 0

        data = {
            "count": count if count else 0,
            "transport_list": transport_list if transport_list else []
        }

        return data
