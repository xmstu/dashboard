from server import log


class OrdersReceivedStatisticsList(object):

    @staticmethod
    def get_order_received_statistics_list(cursor, params):

        fetch_where = """ 1=1 """

        which_table = """ AND 1 """

        command = """
        SELECT
            FROM_UNIXTIME( shb_orders.create_time, '%Y-%m-%d' ) AS create_time,
            COUNT( 1 ) AS order_counts,
            SUM( price ) AS order_sum_price 
        FROM
            `shb_orders`
            INNER JOIN shf_goods ON shf_goods.id = shb_orders.goods_id 
            {which_table}
            WHERE
            {fetch_where}  
        GROUP BY
            FROM_UNIXTIME( shb_orders.create_time, '%Y-%m-%d' )
        """

        # 地区
        region = ' AND 1=1 '
        if params['region_id']:
            if isinstance(params['region_id'], int):
                region = 'AND (shb_orders.from_province_id = %(region_id)s OR shb_orders.from_city_id = %(region_id)s OR shb_orders.from_county_id = %(region_id)s OR shb_orders.from_town_id = %(region_id)s) ' % {
                    'region_id': params['region_id']}
            elif isinstance(params['region_id'], list):
                region = '''
                                AND (
                                shb_orders.from_province_id IN (%(region_id)s)
                                OR shb_orders.from_city_id IN (%(region_id)s)
                                OR shb_orders.from_county_id IN (%(region_id)s)
                                OR shb_orders.from_town_id IN (%(region_id)s)
                                ) ''' % {'region_id': ','.join(params['region_id'])}

        fetch_where += region

        # 时间
        if params.get('start_time') and params.get('end_time'):
            fetch_where += """ AND shb_orders.create_time >= {start_time} AND
            shb_orders.create_time < {end_time} """.format(start_time=params['start_time'], end_time=params['end_time'])

        # 货源类型:同城/跨城/零担
        if params.get('goods_type'):
            fetch_where += """
                AND (
                ({goods_type}=1 AND shf_goods.haul_dist = 1) OR
                ({goods_type}=2 AND shf_goods.haul_dist = 2) OR
                ({goods_type}=3 AND shf_goods.type = 2)
                )
                """.format(goods_type=params['goods_type'])

        # 货源类型:议价/一口价
        if params.get('goods_price_type'):
            fetch_where += """
                    AND (
                    ({goods_price_type}=1 AND shf_goods.goods_level = 1) OR
                    ({goods_price_type}=2 AND shf_goods.is_system_price = 1)
                    )
                    """.format(goods_price_type=params['goods_price_type'])

        # 评价类型
        if params.get('comment_type'):
            which_table += """ LEFT JOIN shu_user_evaluations se on shb_orders.id = se.order_id """
            fetch_where += """ 
            AND( 
                ( {comment_type}=1 AND se.rater_id = shb_orders.driver_id AND se.user_id = shb_orders.owner_id AND se.`level` in (4,5)) OR
                ( {comment_type}=2 AND se.rater_id = shb_orders.driver_id AND se.user_id = shb_orders.owner_id AND se.`level` = 3) OR
                ( {comment_type}=3 AND se.rater_id = shb_orders.driver_id AND se.user_id = shb_orders.owner_id AND se.`level` in (1,2)) OR
                ( {comment_type}=4 AND se.rater_id = shb_orders.owner_id AND se.user_id = shb_orders.driver_id AND se.`level` in (4,5)) OR
                ( {comment_type}=5 AND se.rater_id = shb_orders.owner_id AND se.user_id = shb_orders.driver_id AND se.`level` = 3) OR
                ( {comment_type}=6 AND se.rater_id = shb_orders.owner_id AND se.user_id = shb_orders.driver_id AND se.`level` in (1,2))
             ) """.format(comment_type=params['comment_type'])

        # 支付方式
        if params.get('pay_method'):
            fetch_where += """ 
             AND (
                ( {pay_method}=1 AND shb_orders.pay_status = 1 AND shb_orders.paid_offline = 0) OR
                ( {pay_method}=2 AND shb_orders.pay_status = 2) OR
                ( {pay_method}=3 AND shb_orders.paid_offline = 1)
             )
             """.format(pay_method=params['pay_method'])

        complete_sql = """ AND shb_orders.`status` = 3 """
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
            COUNT(1) as reason_count
        FROM
            `shb_orders`
            LEFT JOIN shf_goods ON shb_orders.goods_id = shf_goods.id 
        WHERE shb_orders.status = -1 AND canceled_user_id != 0
            {fetch_where}
            GROUP BY canceled_reason_text
            ORDER BY reason_count 
        """

        # 地区
        region = ' AND 1=1 '
        if params['region_id']:
            if isinstance(params['region_id'], int):
                region = 'AND (shb_orders.from_province_id = %(region_id)s OR shb_orders.from_city_id = %(region_id)s OR shb_orders.from_county_id = %(region_id)s OR shb_orders.from_town_id = %(region_id)s) ' % {
                    'region_id': params['region_id']}
            elif isinstance(params['region_id'], list):
                region = '''
                        AND (
                        shb_orders.from_province_id IN (%(region_id)s)
                        OR shb_orders.from_city_id IN (%(region_id)s)
                        OR shb_orders.from_county_id IN (%(region_id)s)
                        OR shb_orders.from_town_id IN (%(region_id)s)
                        ) ''' % {'region_id': ','.join(params['region_id'])}

        fetch_where += region

        # 时间
        if params.get('start_time') and params.get('end_time'):
            fetch_where += """
            AND shb_orders.create_time >= {start_time} 
            AND shb_orders.create_time < {end_time}
            """.format(start_time=params['start_time'], end_time=params['end_time'])

        # 货源类型:同城/跨城/零担
        if params.get('goods_type'):
            fetch_where += """
            AND (
            ({goods_type}=1 AND shf_goods.haul_dist = 1) OR
            ({goods_type}=2 AND shf_goods.haul_dist = 2) OR
            ({goods_type}=3 AND shf_goods.type = 2)
            )
            """.format(goods_type=params['goods_type'])

        # 货源类型:议价/一口价
        if params.get('goods_price_type'):
            fetch_where += """
                AND (
                ({goods_price_type}=1 AND shf_goods.goods_level = 1) OR
                ({goods_price_type}=2 AND shf_goods.is_system_price = 1)
                )
                """.format(goods_price_type=params['goods_price_type'])

        # 司机/货主取消
        if params.get('cancel_type'):
            fetch_where += """
            AND (
            ({cancel_type}=1 AND shb_orders.canceled_user_id = shb_orders.driver_id) OR
            ({cancel_type}=2 AND shb_orders.canceled_user_id = shb_orders.owner_id)
            )
            """.format(cancel_type=params['cancel_type'])

        cancel_list_dict = cursor.query(command.format(fetch_where=fetch_where))

        sum_count = 0
        cancel_list = []
        for i in cancel_list_dict:
            if i.get('canceled_reason_text') == '':
                i['canceled_reason_text'] = '未填写取消原因'
            sum_count += i.get('reason_count', None) or 0
            cancel_list.append(list(i.values()))

        for i in cancel_list_dict:
            i.setdefault('percentage', '%.2f%%' % ((i.get('reason_count') / sum_count) * 100))

        data = {
            'cancel_list': cancel_list if cancel_list else [],
            'cancel_list_dict': cancel_list_dict if cancel_list_dict else [{}],
            'sum_count': sum_count
        }

        return data


class OrderListModel(object):

    @staticmethod
    def get_order_list(cursor, page, limit, fresh_ids, params):

        fields = """
                so.id,
                sg.mileage_total,
                sg.NAME,
                sg.weight,
                sg.volume,
                sg.type,
                sg.goods_level,
                sg.is_system_price,
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
                (SELECT level FROM shu_user_evaluations WHERE shu_user_evaluations.rater_id = so.driver_id AND shu_user_evaluations.user_id = so.owner_id AND shu_user_evaluations.order_id = so.id LIMIT 1) AS driver_rate_level,
                (SELECT level FROM shu_user_evaluations WHERE shu_user_evaluations.rater_id = so.owner_id AND shu_user_evaluations.user_id = so.driver_id AND shu_user_evaluations.order_id = so.id LIMIT 1) AS owner_rate_level,
                (SELECT comment FROM shu_user_evaluations WHERE shu_user_evaluations.rater_id = so.driver_id AND shu_user_evaluations.user_id = so.owner_id AND shu_user_evaluations.order_id = so.id LIMIT 1) AS driver_rate_comment,
                (SELECT comment FROM shu_user_evaluations WHERE shu_user_evaluations.rater_id = so.owner_id AND shu_user_evaluations.user_id = so.driver_id AND shu_user_evaluations.order_id = so.id LIMIT 1) AS owner_rate_comment,
                (so.create_time - sg.create_time) as latency_time,
                so.create_time,
            IF
                ( so.STATUS = 3 AND ( so.pay_status = 2 OR so.paid_offline = 1 ), so.update_time, 0 ) AS complete_time,
                (SELECT COUNT(driver_id) from shb_orders WHERE shb_orders.driver_id = so.driver_id) AS c1,
                (SELECT COUNT(1) from shf_goods WHERE shf_goods.user_id = so.owner_id) AS c2,
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
            LEFT JOIN shu_users ON shu_users.id = so.owner_id
        WHERE 
            {fetch_where}
        """

        # 权限地区
        region = ' AND 1=1 '
        if params['node_id']:
            if isinstance(params['node_id'], int):
                region = 'AND (so.from_province_id = %(region_id)s OR so.from_city_id = %(region_id)s OR so.from_county_id = %(region_id)s OR so.from_town_id = %(region_id)s) ' % {
                    'region_id': params['node_id']}
            elif isinstance(params['node_id'], list):
                region = '''
                        AND (
                        so.from_province_id IN (%(region_id)s)
                        OR so.from_city_id IN (%(region_id)s)
                        OR so.from_county_id IN (%(region_id)s)
                        OR so.from_town_id IN (%(region_id)s)
                        ) ''' % {'region_id': ','.join(params['node_id'])}

        fetch_where += region

        # 订单id
        if params.get('order_id'):
            fetch_where += """ AND so.id = {order_id} """.format(order_id=params.get('order_id'))

        # 货主手机
        if params.get('consignor_mobile'):
            fetch_where += """ 
            AND ( SELECT shu_users.mobile FROM shu_users WHERE id = so.owner_id ) = {consignor_mobile} 
            """.format(consignor_mobile=params['consignor_mobile'])

        # 司机手机
        if params.get('driver_mobile'):
            fetch_where += """
            AND ( SELECT shu_users.mobile FROM shu_users WHERE id = so.driver_id ) = {driver_mobile}
            """.format(driver_mobile=params['driver_mobile'])

        # 出发地省份
        if params.get('from_province_id'):
            fetch_where += """
            AND so.from_province_id = {from_province_id}
            """.format(from_province_id=params['from_province_id'])

        # 出发地城市
        if params.get('from_city_id'):
            fetch_where += """
            AND so.from_city_id = {from_city_id}
            """.format(from_city_id=params['from_city_id'])

        # 出发地区县
        if params.get('from_county_id'):
            fetch_where += """
            AND so.from_county_id = {from_county_id}
            """.format(from_county_id=params['from_county_id'])

        # 出发地城镇
        if params.get('from_town_id'):
            fetch_where += """
                AND so.from_town_id = {from_town_id}
                """.format(from_town_id=params['from_town_id'])

        # 目的地省份
        if params.get('to_province_id'):
            fetch_where += """
            AND so.to_province_id = {to_province_id} 
            """.format(to_province_id=params['to_province_id'])

        # 目的地城市
        if params.get('to_city_id'):
            fetch_where += """
            AND so.to_city_id = {to_city_id}
            """.format(to_city_id=params['to_city_id'])

        # 目的地区县
        if params.get('to_county_id'):
            fetch_where += """
            AND so.to_county_id = {to_county_id}
            """.format(to_county_id=params['to_county_id'])

        # 目的地城镇
        if params.get('to_town_id'):
            fetch_where += """
                AND so.to_town_id = {to_town_id}
                """.format(to_town_id=params['to_town_id'])

        # 订单状态
        if params.get('order_status'):
            fetch_where += """
            AND (
            ( {order_status}=1 AND so.`status` in (1,2) ) OR
            ( {order_status}=2 AND so.`status` = 3 ) OR
            ( {order_status}=3 AND so.`status` = -1)
            )
            """.format(order_status=params['order_status'])

        # 订单类型:同城/跨城/零担
        if params.get('order_type'):
            fetch_where += """
            AND (
            ( {order_type}=1 AND sg.haul_dist = 1) OR
            ( {order_type}=2 AND sg.haul_dist = 2) OR
            ( {order_type}=3 AND sg.type = 2)
            )
            """.format(order_type=params['order_type'])

        # 订单类型:议价/一口价
        if params.get('order_price_type'):
            fetch_where += """
            AND (
            ({order_price_type}=1 AND sg.goods_level = 1) OR
            ({order_price_type}=2 AND sg.is_system_price = 1)
            )
            """.format(order_price_type=params['order_price_type'])

        # 车长
        if params.get('vehicle_length'):
            fetch_where += """ AND shf_goods_vehicles.name = '{0}' """.format(params['vehicle_length'])

        # 车型
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

        # 特殊标签
        if params.get('spec_tag'):
            if params['spec_tag'] == 1:
                fetch_where += """ AND so.owner_id IN (%s) """ % ','.join(fresh_ids)

            if params['spec_tag'] == 2:
                fetch_where += """ AND so.driver_id IN (%s) """ % ','.join(fresh_ids)

        # 支付状态
        if params.get('pay_status'):
            fetch_where += """
            AND (
            ({pay_status}=1 AND pay_status = 1 AND paid_offline = 0) OR
            ({pay_status}=2 AND pay_status = 2) OR
            ({pay_status}=3 AND paid_offline = 1)
            )
            """.format(pay_status=params['pay_status'])

        # 是否改价
        if params.get('is_change_price'):
            fetch_where += """
            AND so.price_recommend != so.price AND so.price_recommend != 0
            """

        # 评价级别
        if params.get('comment_type'):
            fetch_where += """
                        AND (
                        ({comment_type}=1 AND se.rater_id = so.driver_id AND se.user_id = so.owner_id AND se.`level` IN (4,5)) OR
                        ({comment_type}=2 AND se.rater_id = so.driver_id AND se.user_id = so.owner_id AND se.`level` = 3) OR
                        ({comment_type}=3 AND se.rater_id = so.driver_id AND se.user_id = so.owner_id AND se.`level` IN (1,2)) OR
                        ({comment_type}=4 AND se.rater_id = so.owner_id AND se.user_id = so.driver_id AND se.`level` IN (4,5)) OR
                        ({comment_type}=5 AND se.rater_id = so.owner_id AND se.user_id = so.driver_id AND se.`level` = 3) OR
                        ({comment_type}=6 AND se.rater_id = so.owner_id AND se.user_id = so.driver_id AND se.`level` IN (1,2))
                        )
                        """.format(comment_type=params['comment_type'])

        # 订单发布时间
        if params.get('start_order_time') and params.get('end_order_time'):
            fetch_where += """
            AND so.create_time >= {0} AND so.create_time < {1}
            """.format(params['start_order_time'], params['end_order_time'])

        # 完成时间
        if params.get('start_complete_time') and params.get('end_complete_time'):
            fetch_where += """
            AND
            IF ( so.STATUS = 3 AND ( so.pay_status = 2 OR so.paid_offline = 1 ), so.update_time, 0 ) >= {0}
            AND 
            IF ( so.STATUS = 3 AND ( so.pay_status = 2 OR so.paid_offline = 1 ), so.update_time, 0 ) < {1}
            """.format(params.get('start_complete_time'), params.get('end_complete_time'))

        # 货主注册时间
        if params.get('register_start_time') and params.get('register_end_time'):
            fetch_where += """
            AND shu_users.create_time >= {0} AND shu_users.create_time < {1}
            """.format(params['register_start_time'], params['register_end_time'])

        fetch_where += """ GROUP BY so.id """

        ret = cursor.query(command.format(fields=" COUNT(1) AS count ", fetch_where=fetch_where))
        count = len(ret)

        fetch_where += """ DESC LIMIT {0}, {1} """.format((page - 1) * limit, limit)

        order_list = cursor.query(command.format(fields=fields, fetch_where=fetch_where))

        data = {
            'count': count,
            'order_list': order_list
        }

        return data


class FreshOwnerModel(object):

    @staticmethod
    def get_fresh_owner_id(bi, db, node_id):
        try:
            # 先找出所有发货小于3的user_id
            good_sql = """
                    SELECT
                        user_id 
                    FROM
                        tb_inf_user 
                    WHERE
                        ( goods_count_LH + goods_count_SH ) < 3 
                        {region}
                    GROUP BY
                        user_id
            """

            # 权限地区
            region = ' AND 1=1 '
            if node_id:
                if isinstance(node_id, int):
                    region = 'AND (from_province_id = %(region_id)s OR from_city_id = %(region_id)s OR from_county_id = %(region_id)s OR from_town_id = %(region_id)s) ' % {
                        'region_id': node_id}
                elif isinstance(node_id, list):
                    region = '''
                            AND (
                            from_province_id IN (%(region_id)s)
                            OR from_city_id IN (%(region_id)s)
                            OR from_county_id IN (%(region_id)s)
                            OR from_town_id IN (%(region_id)s)
                            ) ''' % {'region_id': ','.join(node_id)}

            good_user_ret = bi.query(good_sql.format(region=region))
            good_ret_list = [str(i['user_id']) for i in good_user_ret]
            # 再找出订单列表中发货小于3的owner_id
            order_sql = """SELECT DISTINCT owner_id FROM shb_orders WHERE owner_id IN ( %s )""" % ','.join(good_ret_list)
            log.debug('获取新货主SQL语句：[sql: %s]' % order_sql)
            order_owner_ret = db.query(order_sql)
            ret = [str(i['owner_id']) for i in order_owner_ret]
            return ret
        except Exception as e:
            log.error('Error:{}'.format(e), exc_info=True)

        return ['0']


class FreshDriverModel(object):

    @staticmethod
    def get_fresh_driver_id(cursor, node_id):
        try:
            sql = """
                    SELECT
                        driver_id 
                    FROM
                        shb_orders 
                    WHERE
                        driver_id IN (
                        SELECT DISTINCT
                            driver_id 
                        FROM
                            shb_orders 
                        WHERE
                            {region}
                        ) 
                    GROUP BY
                        driver_id 
                    HAVING
                        COUNT( driver_id ) < 3;
                    """

            # 权限地区
            region = ' 1=1 '
            if node_id:
                if isinstance(node_id, int):
                    region += 'AND (from_province_id = %(region_id)s OR from_city_id = %(region_id)s OR from_county_id = %(region_id)s OR from_town_id = %(region_id)s) ' % {
                        'region_id': node_id}
                elif isinstance(node_id, list):
                    region += '''
                            AND (
                            from_province_id IN (%(region_id)s)
                            OR from_city_id IN (%(region_id)s)
                            OR from_county_id IN (%(region_id)s)
                            OR from_town_id IN (%(region_id)s)
                            ) ''' % {'region_id': ','.join(node_id)}
            ret = cursor.query(sql.format(region=region))
            log.debug('获取新司机SQL语句：[sql: %s]' % sql.format(region=region))
            ret = [str(i['driver_id']) for i in ret]

            return ret
        except Exception as e:
            log.error('Error:{}'.format(e), exc_info=True)

        return ['0']
