

class OrdersReceivedStatisticsList(object):

    @staticmethod
    def get_order_received_statistics_list(cursor, params):

        fetch_where = """
        
        """

        command = """
        SELECT
            FROM_UNIXTIME( shb_orders.create_time, '%Y-%m-%d' ) AS create_time,
            COUNT( * ) as order_counts,
            SUM(price) as order_sum_price
        FROM
            `shb_orders` INNER JOIN shf_goods on shf_goods.id = shb_orders.goods_id
        
        WHERE 
        -- shb_orders.create_time > 1528214400 AND 
        shb_orders.create_time <= 1528941600
        -- 同城 跨城 零担
        AND shf_goods.haul_dist = 1
        -- AND shf_goods.haul_dist = 2
        -- AND shf_goods.type = 2
        
        -- 评价
        
        
        -- 未支付
        -- AND shb_orders.pay_status = 1
        
        -- 线上支付
        -- AND shb_orders.`status` = 3 
        -- AND shb_orders.pay_status = 2 AND shf_goods.payment_method = 1 
        -- 线下支付
        -- AND shb_orders.`status` = 3  
        -- AND shf_goods.payment_method = 2 AND shb_orders.paid_offline = 1
        
        GROUP BY
            FROM_UNIXTIME( shb_orders.create_time, '%Y-%m-%d' )
        """

        data = cursor.query(command)

        return data
