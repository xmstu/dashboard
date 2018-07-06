class HeatMapModel(object):

    @staticmethod
    def get_user(cursor, params):
        fields = """"""

        which_table = """"""

        fetch_where = """ 1=1 """

        command = """
        SELECT
            from_city_id,
            COUNT( 1 ) 
        FROM
            `tb_inf_user` 
        WHERE
            {fetch_where} 
        -- 注册角色是全部/司机/货主/物流公司
        -- 	AND user_type = 3
        -- 认证角色是司机
        -- 	AND driver_auth = 1
        -- 认证角色是货主
        -- 	AND goods_auth = 1
        -- 认证角色是物流公司
        -- 	AND company_auth = 1
        -- 	全部已认证角色
        -- 	AND ( driver_auth = 1 OR goods_auth = 1 OR company_auth = 1 ) 
        -- 活跃数
        -- 	AND keep_login_days >= 7 AND last_login_time > UNIX_TIMESTAMP() - 1 * 86400
            
            AND create_time >= 1395244800 
            AND create_time < 1530633600
            AND from_province_id = 440000 AND from_city_id != 0
            GROUP BY
                from_city_id
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

        # 角色
        if params.get('filter'):
            fetch_where += """"""

        data = cursor.query(command)

        return data

    @staticmethod
    def get_goods(cursor, params):

        fields = """"""

        which_table = """"""

        fetch_where = """"""

        command = """"""

        data = cursor.query(command)

        return data

    @staticmethod
    def get_vehicle(cursor, params):
        fields = """"""

        which_table = """"""

        fetch_where = """"""

        command = """"""

        data = cursor.query(command)

        return data