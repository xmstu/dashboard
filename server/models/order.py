

class OrdersReceivedStatisticsList(object):

    @staticmethod
    def get_order_received_statistics_list(cursor, params):

        fetch_where = """ 1=1 """

        which_table = """ AND 1 """

        command = """
        SELECT
            FROM_UNIXTIME( shb_orders.create_time, '%Y-%m-%d' ) AS create_time,
            COUNT( * ) AS order_counts,
            SUM( price ) AS order_sum_price 
        FROM
            `shb_orders`
            INNER JOIN shf_goods ON shf_goods.id = shb_orders.goods_id 
            {which_table}
            WHERE
            {fetch_where}
        -- 评价 好中差
        -- and shb_orders.owner_id = shu_user_evaluations.user_id
        -- and shb_orders.driver_id = shu_user_evaluations.user_id
        
        -- AND shu_user_evaluations.`level` in (1,2)
        -- AND shu_user_evaluations.`level` = 3
        -- AND shu_user_evaluations.`level` in (4,5)
        
        -- 未支付
        -- AND shb_orders.pay_status = 1
        -- 线上支付
        -- AND shb_orders.`status` = 3 AND shb_orders.pay_status = 2 AND shf_goods.payment_method = 1
        -- 线下支付
        -- AND shb_orders.`status` = 3 AND shf_goods.payment_method = 2 AND shb_orders.paid_offline = 1
            
        GROUP BY
            FROM_UNIXTIME( shb_orders.create_time, '%Y-%m-%d' )
        """

        # 时间
        if params.get('start_time') and params.get('end_time'):
            fetch_where += """ AND shb_orders.create_time >= {start_time} AND
            shb_orders.create_time < {end_time} """.format(start_time=params['start_time'], end_time=params['end_time'])

        # 货源类型
        if params.get('goods_type'):
            fetch_where += """ AND (
            ( {goods_type}=1 AND shf_goods.haul_dist = 1) OR
            ( {goods_type}=2 AND shf_goods.haul_dist = 2) OR
            ( {goods_type}=3 AND shf_goods.type = 2)
            ) """.format(goods_type=params['goods_type'])

        # 地区
        if params.get('region_id'):
            fetch_where += """
                AND ( from_province_id = {region_id} OR from_city_id = {region_id} OR from_county_id = {region_id} ) 
                """.format(region_id=params['region_id'])

        # 评价类型
        if params.get('comment_type'):
            which_table += """ INNER JOIN shu_user_evaluations on shb_orders.id = shu_user_evaluations.order_id """
            fetch_where += """ AND shb_orders.owner_id = shu_user_evaluations.user_id """
            fetch_where += """ 
            AND( 
                ( {comment_type}=1 AND shu_user_evaluations.`level` in (4,5)) OR
                ( {comment_type}=2 AND shu_user_evaluations.`level` = 3) OR
                ( {comment_type}=3 AND shu_user_evaluations.`level` in (1,2))
             ) """.format(comment_type=params['comment_type'])

        # 支付方式
        if params.get('pay_method'):
            fetch_where += """ 
             AND (
                ( {pay_method}=1 AND shb_orders.pay_status = 1 AND shb_orders.paid_offline = 0) OR
                ( {pay_method}=2 AND shb_orders.`status` = 3 AND shb_orders.pay_status = 2 AND shf_goods.payment_method = 1) OR
                ( {pay_method}=3 AND shb_orders.`status` = 3 AND shf_goods.payment_method = 2 AND shb_orders.paid_offline = 1)
             )
             """.format(pay_method=params['pay_method'])

        complete_sql = """
        AND ((shb_orders.`status` = 3 AND shb_orders.pay_status = 2 AND shf_goods.payment_method = 1 ) OR (shb_orders.`status` = 3 AND shf_goods.payment_method = 2 AND shb_orders.paid_offline = 1))
        """
        pending_sql = """ AND shb_orders.`status` IN (1, 2) """
        cancel_sql = """ AND shb_orders.`status` = -1 """

        complete_order = cursor.query(command.format(which_table=which_table, fetch_where=fetch_where + complete_sql))
        pending_order = cursor.query(command.format(which_table=which_table, fetch_where=fetch_where + pending_sql))
        cancel_order = cursor.query(command.format(which_table=which_table, fetch_where=fetch_where + cancel_sql))

        data = {
            'complete_order': complete_order,
            'pending_order': pending_order,
            'cancel_order': cancel_order
        }

        return data


class CancelOrderReasonModel(object):

    @staticmethod
    def get_cancel_order_reason(cursor, params):

        fetch_where = """ AND 1=1 """

        command = """
        SELECT
            shb_orders.canceled_reason_text,
            COUNT(*) as reason_count
        FROM
            `shb_orders`
            LEFT JOIN shf_goods ON shb_orders.goods_id = shf_goods.id 
        WHERE shb_orders.canceled_user_id != 0 AND shb_orders.canceled_reason_id != 0 
            {fetch_where}
            GROUP BY canceled_reason_text
            ORDER BY reason_count 
        """

        # 时间
        if params.get('start_time') and params.get('end_time'):
            fetch_where += """
            AND shb_orders.create_time >= {start_time} 
            AND shb_orders.create_time < {end_time}
            """.format(start_time=params['start_time'], end_time=params['end_time'])

        # 货源类型
        if params.get('goods_type'):
            fetch_where += """
            AND (
            ({goods_type}=1 AND shf_goods.haul_dist = 1) OR
            ({goods_type}=2 AND shf_goods.haul_dist = 2)
            )
            """.format(goods_type=params['goods_type'])

        # 司机/货主取消
        if params.get('cancel_type'):
            fetch_where += """
            AND (
            ({cancel_type}=1 AND shb_orders.canceled_user_id = shb_orders.owner_id ) OR
            ({cancel_type}=2 AND shb_orders.canceled_user_id = shb_orders.driver_id)
            )
            """.format(cancel_type=params['cancel_type'])

        # 地区
        if params.get('region_id'):
            fetch_where += """
            AND (shb_orders.from_province_id = {region_id} or shb_orders.from_city_id = {region_id} or shb_orders.from_county_id = {region_id} or shb_orders.from_county_id={region_id})
            """.format(region_id=params['region_id'])

        cancel_list_dict = cursor.query(command.format(fetch_where=fetch_where))

        sum_count = 0
        cancel_list = []
        for i in cancel_list_dict:
            sum_count += i.get('reason_count', None) or 0
            cancel_list.append(list(i.values()))

        for i in cancel_list_dict:
            i.setdefault('percentage', '%.2f%%' % ((i.get('reason_count') / sum_count) * 100))

        data = {
            'cancel_list': cancel_list if cancel_list else [],
            'cancel_list_dict': cancel_list_dict if cancel_list_dict else [{}]
        }

        return data


class OrderListmodel(object):

    @staticmethod
    def get_order_list(cursor, page, limit, params):

        fields = """
                so.id,
                sg.NAME,
                sg.weight,
                sg.volume,
                sg.type,
                sg.goods_level,
                sg.haul_dist,
                so.from_province_id,
                so.from_city_id,
                so.from_county_id,
                so.from_town_id,
                so.from_address,
                so.to_province_id,
                so.to_city_id,
                so.to_county_id,
                so.to_town_id,
                so.to_address,
                (
                SELECT
                IF
                    ( shf_goods_vehicles.attribute_value_id = 0, '不限车型', GROUP_CONCAT( shm_dictionary_items.`name` ) ) 
                FROM
                    shf_goods_vehicles
                    LEFT JOIN shm_dictionary_items ON shf_goods_vehicles.attribute_value_id = shm_dictionary_items.id 
                    AND shm_dictionary_items.is_deleted = 0 
                WHERE
                    shf_goods_vehicles.goods_id = sg.id 
                    AND shf_goods_vehicles.vehicle_attribute = 1 
                    AND shf_goods_vehicles.is_deleted = 0 
                ) AS vehicle_type,
                shf_goods_vehicles.`name` AS new_vehicle_type,
                so.price,
                ( SELECT shu_users.mobile FROM shu_users WHERE id = so.driver_id ) AS driver_mobile,
                ( SELECT shu_user_profiles.user_name FROM shu_user_profiles WHERE user_id = so.driver_id ) AS driver_name,
                ( SELECT shu_users.mobile FROM shu_users WHERE id = so.owner_id ) AS owner_mobile,
                ( SELECT shu_user_profiles.user_name FROM shu_user_profiles WHERE user_id = so.owner_id ) AS owner_name,
                so.`status`,
                so.pay_status,
                so.paid_offline,
                sg.payment_method,
                se.`level`,
                (so.create_time - sg.create_time) as latency_time,
                so.create_time,
            IF
                ( so.STATUS = 3 AND ( so.pay_status = 2 OR so.paid_offline = 1 ), so.update_time, 0 ) AS complete_time,
                (SELECT COUNT(driver_id) from shb_orders WHERE shb_orders.driver_id = so.driver_id) AS c1,
                (SELECT COUNT(*) from shf_goods WHERE shf_goods.user_id = so.owner_id) AS c2,
                shf_goods_vehicles.need_open_top,
                shf_goods_vehicles.need_tail_board,
                shf_goods_vehicles.need_flatbed,
                shf_goods_vehicles.need_high_sided,
                shf_goods_vehicles.need_box,
                shf_goods_vehicles.need_steel,
                shf_goods_vehicles.need_double_seat,
                shf_goods_vehicles.need_remove_seat
        """

        fetch_where = """ 1=1 """

        command = """
        SELECT
          {fields}
        FROM
            shb_orders AS so
            INNER JOIN shf_goods AS sg ON so.goods_id = sg.id
            LEFT JOIN shf_goods_vehicles ON shf_goods_vehicles.goods_id = sg.id 
            AND shf_goods_vehicles.vehicle_attribute = 3 
            AND shf_goods_vehicles.is_deleted = 0
            LEFT JOIN shu_user_evaluations AS se ON so.id = se.order_id 
        WHERE 
            {fetch_where}
        """

        if params.get('order_id'):
            fetch_where += """ AND so.id = {order_id} """.format(order_id=params.get('order_id'))

        if params.get('consignor_mobile'):
            fetch_where += """ 
            AND ( SELECT shu_users.mobile FROM shu_users WHERE id = so.driver_id ) = {consignor_mobile} 
            """.format(consignor_mobile=params['consignor_mobile'])

        if params.get('driver_mobile'):
            fetch_where += """
            AND ( SELECT shu_users.mobile FROM shu_users WHERE id = so.owner_id ) = {driver_mobile}
            """.format(driver_mobile=params['driver_mobile'])

        if params.get('from_province_id'):
            fetch_where += """
            AND so.from_province_id = {from_province_id}
            """.format(from_province_id=params['from_province_id'])

        if params.get('from_city_id'):
            fetch_where += """
            AND so.from_city_id = {from_city_id}
            """.format(from_city_id=params['from_city_id'])

        if params.get('from_county_id'):
            fetch_where += """
            AND so.from_county_id = {from_county_id}
            """.format(from_county_id=params['from_county_id'])

        if params.get('to_province_id'):
            fetch_where += """
            AND so.to_province_id = {to_province_id} 
            """.format(to_province_id=params['to_province_id'])

        if params.get('to_city_id'):
            fetch_where += """
            AND so.to_city_id = {to_city_id}
            """.format(to_city_id=params['to_city_id'])

        if params.get('to_county_id'):
            fetch_where += """
            AND so.to_county_id = {to_county_id}
            """.format(to_county_id=params['to_county_id'])

        if params.get('order_status'):
            fetch_where += """
            AND (
            ( {order_status}=1 AND so.`status` not in (0, -1) AND so.pay_status = 1 AND so.paid_offline = 0) OR
            ( {order_status}=2 AND so.`status` = 3 AND ( so.pay_status = 2 OR so.paid_offline = 1 )) OR
            ( {order_status}=3 AND so.`status` = -1)
            )
            """.format(order_status=params['order_status'])

        if params.get('order_type'):
            fetch_where += """
            AND (
            ( {order_type}=1 AND sg.haul_dist = 1 AND sg.type = 1) OR
            ( {order_type}=2 AND sg.haul_dist = 2 AND sg.goods_level = 2 AND sg.type = 1) OR
            ( {order_type}=3 AND sg.haul_dist = 2 AND sg.goods_level = 1 AND sg.type = 1) OR
            ( {order_type}=4 AND sg.type = 2)
            )
            """.format(order_type=params['order_type'])

        if int(params.get('vehicle_length')):
            fetch_where += """
            AND shf_goods_vehicles.name = '{0}'
            """.format(params['vehicle_length'])

        if params.get('vehicle_type'):
            fetch_where += """
            AND (
            ( {vehicle_type}=1 AND shf_goods_vehicles.need_open_top = 1) OR
            ( {vehicle_type}=2 AND shf_goods_vehicles.need_tail_board = 1) OR
            ( {vehicle_type}=3 AND shf_goods_vehicles.need_flatbed = 1) OR
            ( {vehicle_type}=4 AND shf_goods_vehicles.need_high_sided = 1) OR
            ( {vehicle_type}=5 AND shf_goods_vehicles.need_box = 1) OR
            ( {vehicle_type}=6 AND shf_goods_vehicles.need_steel = 1) OR
            ( {vehicle_type}=7 AND shf_goods_vehicles.need_double_seat = 1) OR
            ( {vehicle_type}=8 AND shf_goods_vehicles.need_remove_seat = 1) 
            )
            """.format(vehicle_type=params['vehicle_type'])

        # 网点
        if params.get('node_id'):
            if isinstance(params['node_id'], int):
                fetch_where += """ 
                AND (sg.from_province_id = {0}
                OR sg.from_city_id = {0}
                OR sg.from_county_id = {0}
                OR sg.from_town_id = {0})
                """.format(params['node_id'])
            elif isinstance(params['node_id'], list):
                fetch_where += """ 
                AND (sg.from_province_id IN ({0})
                OR sg.from_city_id IN ({0})
                OR sg.from_county_id IN ({0})
                OR sg.from_town_id IN ({0}))
                """.format(','.join(params['node_id']))

        if params.get('spec_tag'):
            fetch_where += """
            AND(
            ( {spec_tag}=1 AND (SELECT COUNT(driver_id) from shb_orders WHERE shb_orders.driver_id = so.driver_id) < 3) OR
            ( {spec_tag}=2 AND (SELECT COUNT(*) from shf_goods WHERE shf_goods.user_id = so.owner_id) < 3)
            )
            """.format(spec_tag=params['spec_tag'])

        if params.get('pay_status'):
            fetch_where += """
            AND (
            ({pay_status}=1 AND pay_status = 1 AND paid_offline = 0) OR
            ({pay_status}=2 AND pay_status = 2) OR
            ({pay_status}=3 AND paid_offline = 1)
            )
            """.format(pay_status=params['pay_status'])

        if params.get('is_change_price'):
            fetch_where += """
            AND so.price_recommend != price AND so.price_recommend != 0
            """

        if params.get('comment_type'):
            fetch_where += """
                        AND (
                        ({comment_type}=1 AND se.`level` IN (4,5)) OR
                        ({comment_type}=2 AND se.`level` = 3) OR
                        ({comment_type}=3 AND se.`level` IN (1,2))
                        )
                        """.format(comment_type=params['comment_type'])

        if params.get('start_order_time') and params.get('end_order_time'):
            fetch_where += """
            AND so.create_time >= {0} AND so.create_time < {1}
            """.format(params['start_order_time'], params['end_order_time'])

        if params.get('start_loading_time') and params.get('end_loading_time'):
            fetch_where += """
            AND ((sg.loading_time_period_end >={0} AND sg.loading_time_period_end < {1}) OR (UNIX_TIMESTAMP(sg.loading_time_date) >={0} AND UNIX_TIMESTAMP(sg.loading_time_date) < {1}))
            """.format(params.get('start_loading_time'), params.get('end_loading_time'))

        count = cursor.query_one(command.format(fields=" COUNT(*) AS total_count ", fetch_where=fetch_where))['total_count']

        fetch_where += """ ORDER BY id DESC LIMIT {0}, {1} """.format((page - 1) * limit, limit)

        order_list = cursor.query(command.format(fields=fields, fetch_where=fetch_where))

        data = {
            'count': count,
            'order_list': order_list
        }

        return data