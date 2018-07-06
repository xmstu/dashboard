import time


class HeatMapModel(object):

    @staticmethod
    def get_user(cursor, params):
        fields = """"""

        fetch_where = """ 1=1 """

        command = """
        SELECT
            from_city_id,
            COUNT( 1 ) 
        FROM
            `tb_inf_user` 
        WHERE
            {fetch_where} 
            AND create_time >= :start_time 
            AND create_time < :end_time
            AND from_province_id = 440000 AND from_city_id != 0
            GROUP BY
                from_city_id
        """
        # 地区
        region = ' AND 1=1 '
        if params['region_id']:
            if isinstance(params['region_id'], int):
                region = 'AND (tb_inf_user.from_province_id = %(region_id)s OR tb_inf_user.from_city_id = %(region_id)s OR tb_inf_user.from_county_id = %(region_id)s OR tb_inf_user.from_town_id = %(region_id)s) ' % {
                    'region_id': params['region_id']}
            elif isinstance(params['region_id'], list):
                region = '''
                        AND (
                        tb_inf_user.from_province_id IN (%(region_id)s)
                        OR tb_inf_user.from_city_id IN (%(region_id)s)
                        OR tb_inf_user.from_county_id IN (%(region_id)s)
                        OR tb_inf_user.from_town_id IN (%(region_id)s)
                        ) ''' % {'region_id': ','.join(params['region_id'])}

        fetch_where += region

        # 角色
        if params.get('filter'):
            fetch_where += """
            AND 
            (
            ( {filter}=1 AND user_type = 1) OR
            ( {filter}=2 AND user_type = 2) OR
            ( {filter}=3 AND user_type = 3) 
            )
            """.format(filter=params['filter'])

        # 字段
        if params.get('field'):
            # 求用户总数
            if params['field'] == 1:
                pass
            # 求角色对应的认证数
            elif params['field'] == 2:
                if params.get('filter') == 1:
                    fetch_where += """
                    AND driver_auth = 1
                    """
                elif params.get('filter') == 2:
                    fetch_where += """
                    AND goods_auth = 1
                    """
                elif params.get('filter') == 3:
                    fetch_where += """
                    AND company_auth = 1
                    """
                else:
                    fetch_where += """
                    AND ( driver_auth = 1 OR goods_auth = 1 OR company_auth = 1 ) 
                    """
            # 求活跃数
            elif params['field'] == 3:
                fetch_where += """
                AND keep_login_days >= 7 AND last_login_time > UNIX_TIMESTAMP() - 86400
                """

        kwargs = {
            "start_time": params.get('start_time', time.time() - 86400*7),
            "end_time": params.get('end_time', time.time() - 86400)
        }

        data = cursor.query(command, kwargs)

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