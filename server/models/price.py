class PriceTrendModel(object):

    @staticmethod
    def get_data(cursor, params):

        fields = """"""

        which_table = """"""

        fetch_where = """"""

        command = """
        SELECT
            FROM_UNIXTIME(so.create_time,"%%Y-%%m-%%d") create_time,
            MAX(price) max_price,
            MIN(price) min_price
        FROM
        shb_orders so INNER JOIN shf_goods sg ON so.goods_id = sg.id
        LEFT JOIN shf_goods_vehicles ON shf_goods_vehicles.goods_id = sg.id 
        AND shf_goods_vehicles.vehicle_attribute = 3 
        AND shf_goods_vehicles.is_deleted = 0
        WHERE
        1=1
        -- 出发地和目的地
        AND so.from_province_id = 440000
        AND so.from_city_id = 440100
        AND so.from_county_id = 440106
        AND so.to_province_id = 440000
        AND so.to_city_id = 440300
        AND so.to_county_id = 440306
        -- 里程
        AND sg.mileage_total >= 0 
        AND sg.mileage_total < 100000
        AND shf_goods_vehicles.`name` = '4.2米'
        -- 线上支付
        AND pay_status = 2
        -- 线下支付
        -- AND paid_offline = 1
        -- 时间
        AND so.create_time >= :start_time 
        AND so.create_time < :end_time
        GROUP BY
            FROM_UNIXTIME(so.create_time,"%%Y-%%m-%%d")
        """

        data = cursor.query(command)

        return data