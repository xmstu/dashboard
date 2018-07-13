import json
import time
from server.utils.extend import data_price, ExtendHandler


class PriceTrendModel(object):

    @staticmethod
    def get_data(cursor, params):
        fetch_where = """ 1=1 """

        command = """
        SELECT
            FROM_UNIXTIME(so.create_time,"%%Y-%%m-%%d") create_time,
            MAX(price) max_price,
            MIN(price) min_price,
            AVG(sg.mileage_total) avg_mileage
        FROM
            shb_orders so 
            INNER JOIN shf_goods sg ON so.goods_id = sg.id
            LEFT JOIN shf_goods_vehicles ON shf_goods_vehicles.goods_id = sg.id 
            AND shf_goods_vehicles.vehicle_attribute = 3 
            AND shf_goods_vehicles.is_deleted = 0
        WHERE
        {fetch_where}
        -- 时间
        AND so.create_time >= :start_time 
        AND so.create_time < :end_time
        -- 车长
        AND shf_goods_vehicles.`name` = :vehicle_length
        GROUP BY
            FROM_UNIXTIME(so.create_time,"%%Y-%%m-%%d")
        """

        # 权限地区
        region = ' AND 1=1 '
        if params['region_id']:
            if isinstance(params['region_id'], int):
                region = 'AND (so.from_province_id = %(region_id)s OR so.from_city_id = %(region_id)s OR so.from_county_id = %(region_id)s OR so.from_town_id = %(region_id)s) ' % {
                    'region_id': params['region_id']}
            elif isinstance(params['region_id'], list):
                region = '''
                            AND (
                            so.from_province_id IN (%(region_id)s)
                            OR so.from_city_id IN (%(region_id)s)
                            OR so.from_county_id IN (%(region_id)s)
                            OR so.from_town_id IN (%(region_id)s)
                            ) ''' % {'region_id': ','.join(params['region_id'])}

        fetch_where += region

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

        # 里程
        if params.get('min_mileage'):
            fetch_where += """ AND sg.mileage_total >= {min_mileage} """.format(min_mileage=params['min_mileage'])

        if params.get('max_mileage'):
            fetch_where += """ AND sg.mileage_total < {max_mileage} """.format(max_mileage=params['max_mileage'])

        # 支付方式
        if params.get('pay_method'):
            fetch_where += """
            AND (
            ( {pay_method}=1 AND pay_status = 2) OR
            ( {pay_method}=2 AND paid_offline = 1)
            )
            """.format(pay_method=params['pay_method'])

        # 时间和车长
        kwargs = {
            'start_time': params.get('start_time', time.time() - 86400 * 7),
            'end_time': params.get('end_time', time.time() - 86400),
            'vehicle_length': params.get('vehicle_length', '小面包车')
        }

        price_trend = cursor.query(command.format(fetch_where=fetch_where), kwargs)
        price_trend = json.loads(json.dumps(price_trend, default=ExtendHandler.handler_to_float))
        # 获取价格基准线
        recommend_price_instance = data_price[params['vehicle_length']]
        recommend_price_one = recommend_price_instance.get_fast_price(params['min_mileage'])
        recommend_price_two = recommend_price_instance.get_fast_price(params['max_mileage'])
        if price_trend:
            if params.get('from_province_id') and params.get('to_province_id'):
                recommend_price_one = recommend_price_instance.get_fast_price(price_trend[0]['avg_mileage'])
                recommend_price_two = 0
        else:
            price_trend = []
            recommend_price_one = 0
            recommend_price_two = 0

        data = {
            "price_trend": price_trend,
            "recommend_price_one": recommend_price_one,
            "recommend_price_two": recommend_price_two,
        }

        return data
