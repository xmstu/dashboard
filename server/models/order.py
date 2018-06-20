

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
            shb_orders.create_time <= {end_time} """.format(start_time=params['start_time'], end_time=params['end_time'])

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
                ( {comment_type}=1 AND shu_user_evaluations.`level` in (1,2)) OR
                ( {comment_type}=2 AND shu_user_evaluations.`level` = 3) OR
                ( {comment_type}=3 AND shu_user_evaluations.`level` in (4,5))
             ) """.format(comment_type=params['comment_type'])

        # 支付方式
        if params.get('pay_method'):
            fetch_where += """ 
             AND (
                ( {pay_method}=1 AND shb_orders.pay_status = 1) OR
                ( {pay_method}=2 AND shb_orders.`status` = 3 AND shb_orders.pay_status = 2 AND shf_goods.payment_method = 1) OR
                ( {pay_method}=3 AND shb_orders.`status` = 3 AND shf_goods.payment_method = 2 AND shb_orders.paid_offline = 1)
             )
             """.format(pay_method=params['pay_method'])

        order_received_statistics_list = cursor.query(command.format(which_table=which_table, fetch_where=fetch_where))

        data = {
            'data': order_received_statistics_list
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
            AND shb_orders.create_time <= {end_time}
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