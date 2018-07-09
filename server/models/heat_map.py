import time


class HeatMapModel(object):

    @staticmethod
    def get_user(cursor, params, level):
        fields = """"""

        fetch_where = """ 1=1 """

        command = """
        SELECT
            :region_group,
            COUNT( 1 ) 
        FROM
            `tb_inf_user` 
        WHERE
            {fetch_where} 
            AND create_time >= :start_time 
            AND create_time < :end_time
            GROUP BY
              :region_group
        """

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

        # 根据级别分组数据
        if level == 1:
            group_condition = 'from_province_id'
            region_group = 'from_province_id'
        elif level == 2:
            group_condition = 'from_province_id'
            region_group = 'from_city_id'
        elif level == 3:
            group_condition = 'from_city_id'
            region_group = 'from_county_id'
        else:
            group_condition = ''
            region_group = ''

        # 根据地区id获取数据
        if int(params.get('region_id')):
            fetch_where += """ AND {group_condition} = {region_id} """.format(group_condition=group_condition, region_id=params['region_id'])

        fetch_where += """ AND {group_condition} != 0 """.format(group_condition=group_condition)

        kwargs = {
            "start_time": params.get('start_time', time.time() - 86400*7),
            "end_time": params.get('end_time', time.time() - 86400),
            "group_condition": group_condition,
            "region_group": region_group
        }

        data = cursor.query(command.format(fetch_where=fetch_where), kwargs)

        return data

    @staticmethod
    def get_goods(cursor, params):

        fields = """"""

        which_table = """"""

        fetch_where = """"""

        command = """
        SELECT
            sg.from_city_id,
            COUNT( 1 ),
            COALESCE ( SUM( price_expect + price_addition ), 0 ),
            COUNT( so.id ),
            COALESCE ( SUM( so.price ), 0 ) 
        FROM
            shf_goods sg
            LEFT JOIN shb_orders so ON so.goods_id = sg.id 
        WHERE
            1 = 1 
        -- 业务类型
        -- 	AND haul_dist = 1
            AND haul_dist = 2 
            AND sg.create_time >= 1395244800 
            AND sg.create_time < 1530633600 
            AND sg.from_province_id = 440000
        GROUP BY
            sg.from_city_id;
        """

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