from server import log
from server.meta.redis_cache import redis_cache


class FreshModel(object):

    @staticmethod
    @redis_cache(1800, owner="new")
    def get_fresh_consignor_id(cursor, region_id):
        try:
            # 先找出所有下单少于三次的用户id的结果集
            sql = """
                    SELECT
                        user_id 
                    FROM
                        shf_goods 
                    WHERE
                        user_id IN (
                        SELECT DISTINCT
                            user_id 
                        FROM
                            shf_goods 
                        WHERE
                            {region}
                        ) 
                    GROUP BY
                        user_id 
                    HAVING
                        COUNT( * ) < 3;
                    """
            # 地区
            region = ' 1=1 '
            if region_id:
                if isinstance(region_id, int):
                    region += 'AND (from_province_id = %(region_id)s OR from_city_id = %(region_id)s OR from_county_id = %(region_id)s OR from_town_id = %(region_id)s) ' % {
                        'region_id': region_id}
                elif isinstance(region_id, list):
                    region += '''
                            AND (
                            from_province_id IN (%(region_id)s)
                            OR from_city_id IN (%(region_id)s)
                            OR from_county_id IN (%(region_id)s)
                            OR from_town_id IN (%(region_id)s)
                            ) ''' % {'region_id': ','.join(region_id)}
            ret = cursor.query(sql.format(region=region))
            user_id_list = [str(i['user_id']) for i in ret]
            return user_id_list
        except Exception as e:
            log.error('Error:{}'.format(e), exc_info=True)
            return ['0']

    @staticmethod
    @redis_cache(1800, driver="new")
    def get_fresh_driver_id(cursor, region_id):
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
            if region_id:
                if isinstance(region_id, int):
                    region += """AND (
                                from_province_id = %(region_id)s 
                                OR from_city_id = %(region_id)s 
                                OR from_county_id = %(region_id)s 
                                OR from_town_id = %(region_id)s) """ % {'region_id': region_id}
                elif isinstance(region_id, list):
                    region += '''
                            AND (
                            from_province_id IN (%(region_id)s)
                            OR from_city_id IN (%(region_id)s)
                            OR from_county_id IN (%(region_id)s)
                            OR from_town_id IN (%(region_id)s)
                            ) ''' % {'region_id': ','.join(region_id)}
            ret = cursor.query(sql.format(region=region))
            log.debug('获取新司机SQL语句：[sql: %s]' % sql.format(region=region))
            ret = [str(i['driver_id']) for i in ret]

            return ret
        except Exception as e:
            log.error('Error:{}'.format(e), exc_info=True)

        return ['0']
