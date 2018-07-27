from server import log
from server.cache_data import vehicle_id_list
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
            AND vehicle.vehicle_length_id = "{vehicle_id}"
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
    def get_data(cursor1, cursor2, page, limit, params):

        filelds = """goods.*, IF ( orders.order_count, orders.order_count, 0 ) order_count"""

        good_fetch_where = """ 1=1 """
        vehicle_fetch_where = """ 1=1 """
        order_fetch_where = """ 1=1 """

        cmd1 = """ 
        SELECT
          {filelds}
        FROM 
        (SELECT
            FROM_UNIXTIME(sg.create_time, "%%Y-%%m-%%d") as create_time,
            sg.from_province_id,
            sg.from_city_id,
            sg.to_province_id,
            sg.to_city_id,
            AVG(mileage_total) AS avg_mileage_total,
            COUNT(sg.id) AS goods_count
        FROM
            shf_goods sg
            LEFT JOIN shf_goods_vehicles ON shf_goods_vehicles.goods_id = sg.id 
            AND shf_goods_vehicles.vehicle_attribute = 3 
            AND shf_goods_vehicles.is_deleted = 0 
        WHERE
            {good_fetch_where}
            AND sg.is_deleted = 0
            -- 时间
            AND sg.create_time >= :start_time 
            AND sg.create_time < :end_time
            GROUP BY 
            FROM_UNIXTIME(sg.create_time, "%%Y-%%m-%%d"),
            sg.from_province_id,
            sg.from_city_id,
            sg.to_province_id,
            sg.to_city_id) AS goods LEFT JOIN
            (
            SELECT
                FROM_UNIXTIME(so.create_time, "%%Y-%%m-%%d") as create_time,
                so.from_province_id,
                so.from_city_id,
                so.to_province_id,
                so.to_city_id,
                COUNT( so.id ) order_count
            FROM
                shb_orders so INNER JOIN shf_goods sg ON sg.id = so.goods_id
                LEFT JOIN shf_goods_vehicles ON shf_goods_vehicles.goods_id = so.goods_id 
                AND shf_goods_vehicles.vehicle_attribute = 3 
                AND shf_goods_vehicles.is_deleted = 0 
            WHERE
                {order_fetch_where}
                AND so.is_deleted = 0 AND so.`status` != -1
                AND so.create_time >= :start_time
                AND so.create_time < :end_time
            GROUP BY 
                FROM_UNIXTIME(so.create_time, "%%Y-%%m-%%d"),
                so.from_province_id,
                so.from_city_id,
                so.to_province_id,
                so.to_city_id
            ) AS orders USING(
            create_time,
            from_province_id,
            from_city_id,
            to_province_id,
            to_city_id
            )
        """

        cmd2 = """
        SELECT
            vehicle.create_time,
            vehicle.from_province_id,
            vehicle.from_city_id,
            vehicle.to_province_id,
            vehicle.to_city_id,
            {vehicle_count} vehicle_count
        FROM
            `tb_inf_transport_vehicles` vehicle
            LEFT JOIN tb_inf_user user USING(user_id)
        WHERE
            {vehicle_fetch_where}
            AND UNIX_TIMESTAMP(vehicle.create_time) < :end_time
            AND vehicle.vehicle_length_id != ''
        GROUP BY
            vehicle.create_time,
            vehicle.from_province_id,
            vehicle.from_city_id,
            vehicle.to_province_id,
            vehicle.to_city_id
        """

        # 地区权限
        good_region = vehicle_region = order_region =' AND 1=1 '
        if params['region_id']:
            if isinstance(params['region_id'], int):
                good_region = 'AND (sg.from_province_id = %(region_id)s OR sg.from_city_id = %(region_id)s OR sg.from_county_id = %(region_id)s OR sg.from_town_id = %(region_id)s) ' % {
                    'region_id': params['region_id']}
                vehicle_region = 'AND (vehicle.from_province_id = %(region_id)s OR vehicle.from_city_id = %(region_id)s OR vehicle.from_county_id = %(region_id)s OR vehicle.from_town_id = %(region_id)s) ' % {
                    'region_id': params['region_id']}
                order_region = 'AND (so.from_province_id = %(region_id)s OR so.from_city_id = %(region_id)s OR so.from_county_id = %(region_id)s OR so.from_town_id = %(region_id)s) ' % {
                    'region_id': params['region_id']}
            elif isinstance(params['region_id'], list):
                good_region = '''
                        AND (
                        sg.from_province_id IN (%(region_id)s)
                        OR sg.from_city_id IN (%(region_id)s)
                        OR sg.from_county_id IN (%(region_id)s)
                        OR sg.from_town_id IN (%(region_id)s)
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
                        so.from_province_id IN (%(region_id)s)
                        OR so.from_city_id IN (%(region_id)s)
                        OR so.from_county_id IN (%(region_id)s)
                        OR so.from_town_id IN (%(region_id)s)
                        ) ''' % {'region_id': ','.join(params['region_id'])}
        good_fetch_where += good_region
        vehicle_fetch_where += vehicle_region
        order_fetch_where += order_region

        # 出发地
        # if params['from_county_id']:
        #     good_fetch_where += ' AND sg.from_county_id = %d ' % params['from_county_id']
        #     vehicle_fetch_where += ' AND vehicle.from_county_id = %d ' % params['from_county_id']
        if params['from_city_id']:
            good_fetch_where += ' AND sg.from_city_id = %d ' % params['from_city_id']
            vehicle_fetch_where += ' AND vehicle.from_city_id = %d ' % params['from_city_id']
            order_fetch_where += ' AND so.from_city_id = %d ' % params['from_city_id']
        if params['from_province_id']:
            good_fetch_where += ' AND sg.from_province_id = %d ' % params['from_province_id']
            vehicle_fetch_where += ' AND vehicle.from_province_id = %d ' % params['from_province_id']
            order_fetch_where += ' AND so.from_province_id = %d ' % params['from_province_id']

        # 目的地
        # if params['to_county_id']:
        #     good_fetch_where += ' AND sg.to_county_id = %d ' % params['to_county_id']
        #     vehicle_fetch_where += ' AND vehicle.to_county_id = %d ' % params['to_county_id']
        if params['to_city_id']:
            good_fetch_where += ' AND sg.to_city_id = %d ' % params['to_city_id']
            vehicle_fetch_where += ' AND vehicle.to_city_id = %d ' % params['to_city_id']
            order_fetch_where += ' AND so.to_city_id = %d ' % params['to_city_id']
        if params['to_province_id']:
            good_fetch_where += ' AND sg.to_province_id = %d ' % params['to_province_id']
            vehicle_fetch_where += ' AND vehicle.to_province_id = %d ' % params['to_province_id']
            order_fetch_where += ' AND so.to_province_id = %d ' % params['to_province_id']

        # 车长要求
        if params['vehicle_length']:
            good_fetch_where += """ AND shf_goods_vehicles.`name` = '%s' """ % params['vehicle_length']
            order_fetch_where += """ AND shf_goods_vehicles.`name` = '%s' """ % params['vehicle_length']
            vehicle_fetch_where += """ AND vehicle.vehicle_length_id = "{vehicle_id}" """.format(vehicle_id=vehicle_name_id.get(params['vehicle_length'], '小面包车'))

        # # 业务类型:同城/跨城/零担
        # if params['business']:
        #     good_fetch_where += """
        #     AND (({business}=1 AND haul_dist = 1) OR ({business}=2 AND haul_dist = 2) OR ({business}=3 AND sg.type = 2))
        #     """.format(business=params['business'])
        #
        # # 业务类型:议价/一口价
        # if params['business_price']:
        #     good_fetch_where += """
        #     AND (({business_price}=1 AND sg.goods_level = 1) OR ({business_price}=2 AND sg.is_system_price = 1))
        #     """.format(business_price=params['business_price'])

        # 时间
        kwargs = {
            'start_time': params.get('start_time', 0),
            'end_time': params.get('end_time', 0)
        }

        count = cursor1.query_one(cmd1.format(filelds=""" COUNT(1) AS count """, good_fetch_where=good_fetch_where, order_fetch_where=order_fetch_where), kwargs)['count']

        cmd1 += """ ORDER BY create_time DESC LIMIT %s, %s """ % ((page - 1) * limit, limit)

        transport_list = cursor1.query(cmd1.format(filelds=filelds, good_fetch_where=good_fetch_where, order_fetch_where=order_fetch_where), kwargs)

        vehicle_all_list = cursor2.query(cmd2.format(vehicle_count="COUNT( DISTINCT user_id )", vehicle_fetch_where=vehicle_fetch_where), kwargs)

        vehicle_fetch_where += """
        AND UNIX_TIMESTAMP(vehicle.create_time) >= :start_time
        AND user.last_login_time >= :start_time 
        AND user.last_login_time < :end_time
        """
        vehicle_list = cursor2.query(cmd2.format(vehicle_count="COUNT( 1 )", vehicle_fetch_where=vehicle_fetch_where), kwargs)

        for i in transport_list:
            vehicle_all_count = [j['vehicle_count'] for j in vehicle_all_list if
                             i['create_time'] == j['create_time'] and
                             i['from_province_id'] == j['from_province_id'] and i['from_city_id'] == j['from_city_id']
                             and i['to_province_id'] == j['to_province_id'] and i['to_city_id'] == j['to_city_id']
                             ]

            if vehicle_all_count:
                i['vehicle_all_count'] = vehicle_all_count[0]
            else:
                i['vehicle_all_count'] = 0

            vehicle_count = [j['vehicle_count'] for j in vehicle_list if
                             i['create_time'] == j['create_time'] and
                             i['from_province_id'] == j['from_province_id'] and i['from_city_id'] == j['from_city_id']
                             and i['to_province_id'] == j['to_province_id'] and i['to_city_id'] == j['to_city_id']
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
