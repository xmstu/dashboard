class GoodsPotentialDistributionTrendModel(object):

    @staticmethod
    def get_data(cursor, params):

        fields = """"""

        which_table = """"""

        fetch_where = """"""

        command = """"""

        data = cursor.query(command)

        return data


class GoodsPotentialListModel(object):

    @staticmethod
    def get_ftl_data(cursor, page, limit, params):

        fields = """
        `name`,
        weight,
        volume,
        is_system_price,
        haul_dist,
        from_province_id,
        from_city_id,
        from_county_id,
        from_town_id,
        from_address,
        to_province_id,
        to_city_id,
        to_county_id,
        to_town_id,
        to_address,
        mileage_total,
        vehicle_name,
        need_open_top,
        need_tail_board,
        need_flatbed,
        need_high_sided,
        need_box,
        need_steel,
        need_double_seat,
        need_remove_seat,
        IF(price_expect,price_expect,price_recommend) AS price,
        loading_time_period_begin,
        -- 用户信息
        mobile,
        user_name,
        ( SELECT COUNT( 1 ) FROM shf_goods WHERE user_id = shu_users.id ) goods_counts,
        ( SELECT COUNT(1) FROM shb_orders WHERE owner_id = shu_users.id AND `status` = 3)  orders_counts,
        FROM_UNIXTIME(shu_users.create_time, '%Y-%m-%d') register_time
        """

        fetch_where = """1=1"""

        command = """
        SELECT
            {fields}
        FROM
            `shf_potential_goods`
            INNER JOIN shu_users ON shu_users.id = shf_potential_goods.user_id
            INNER JOIN shu_user_profiles ON shu_user_profiles.user_id = shu_users.id
        WHERE
            {fetch_where}
        """
        # 地区权限
        region = ' AND 1=1 '
        if params['region_id'] and isinstance(params['region_id'], list):
            region = '''
                    AND (
                    from_province_id IN (%(region_id)s)
                    OR from_city_id IN (%(region_id)s)
                    OR from_county_id IN (%(region_id)s)
                    OR from_town_id IN (%(region_id)s)
                    ) ''' % {'region_id': ','.join(params['region_id'])}

        fetch_where += region

        # 直接过滤的字段
        svs_list = ('from_province_id', 'from_city_id', 'from_county_id', 'from_town_id',
                    'to_province_id', 'to_city_id', 'to_county_id', 'to_town_id', 'vehicle_name')

        for key, value in params.items():
            if key in svs_list and value and isinstance(value, int):
                fetch_where += ' AND {key} = {value}'.format(key=key, value=value)
            elif key in svs_list and value and isinstance(value, str):
                fetch_where += " AND {key} = '{value}'".format(key=key, value=value)

        # 货源类型 一口价/议价
        if params.get('goods_type'):
            fetch_where += """
             AND (
                ({goods_type}=1 AND is_system_price = 1) OR
                ({goods_type}=2 AND is_system_price = 0) 
                )
            """.format(goods_type=params['goods_type'])

        # 距离类型
        if params.get('haul_dist'):
            fetch_where += """
            AND (
                ({haul_dist}=1 AND haul_dist = 1) OR
                ({haul_dist}=2 AND haul_dist = 2) 
            )
            """.format(haul_dist=params['haul_dist'])

        # 特殊条件
        if params.get('special_tag'):
            fetch_where += """
            AND (
                ({special_tag}=1 AND shu_users.create_time > UNIX_TIMESTAMP(DATE(NOW())) AND shu_users.create_time < UNIX_TIMESTAMP()) OR
                ({special_tag}=2 AND ( SELECT COUNT( 1 ) FROM shf_goods WHERE user_id = shu_users.id ) > 0) OR
                ({special_tag}=3 AND ( SELECT COUNT(1) FROM shb_orders WHERE owner_id = shu_users.id AND `status` = 3) > 0) OR
                ({special_tag}=4 AND ( SELECT COUNT(1) FROM shb_orders WHERE owner_id = shu_users.id AND `status` = 3) = 0) 
                )
            """.format(special_tag=params['special_tag'])

        # 根据注册时间
        if params.get('register_start_time') and params.get('register_end_time'):
            fetch_where += """
            AND shu_users.create_time > {0}
            AND	shu_users.create_time <= {1}
            """.format(params['register_start_time'], params['register_end_time'])

        # 根据记录生成时间
        if params.get('record_start_time') and params.get('record_end_time'):
            fetch_where += """
            AND shf_potential_goods.create_time > {0}
            AND shf_potential_goods.create_time <= {1}
            """.format(params['record_start_time'], params['record_end_time'])

        count = cursor.query_one(command.format(fields='COUNT(1) AS count', fetch_where=fetch_where))['count']

        command += 'ORDER BY shf_potential_goods.id DESC LIMIT %s, %s' % ((page - 1) * limit, limit)

        ftl_data = cursor.query(command.format(fields=fields, fetch_where=fetch_where))

        data = {
            'potential_data': ftl_data if ftl_data else [],
            'count': count if count else 0
        }

        return data

    @staticmethod
    def get_ltl_data(cursor, page, limit, params):
        fields = """
            '' AS name,
            weight,
            volume,
            '零担' AS goods_type,
            from_province_id,
            from_city_id,
            from_county_id,
            from_town_id,
            from_address,
            to_province_id,
            to_city_id,
            to_county_id,
            to_town_id,
            to_address,
            0 AS mileage_total,
            '' AS vehicle_name,
            freight_ftl+freight_collect AS price,
            '' AS loading_time_begin,
            mobile,
            user_name,
            ( SELECT COUNT( 1 ) FROM shf_goods WHERE user_id = shu_users.id ) goods_counts,
            ( SELECT COUNT(1) FROM shb_orders WHERE owner_id = shu_users.id AND `status` = 3)  orders_counts,
            FROM_UNIXTIME(shu_users.create_time, '%Y-%m-%d') register_time
        """

        fetch_where = """1=1"""

        command = """
        SELECT
            {fields}
        FROM
            shf_ltl_pre_goods
            INNER JOIN shu_users ON shu_users.id = shf_ltl_pre_goods.user_id
            INNER JOIN shu_user_profiles ON shu_user_profiles.user_id = shu_users.id
        WHERE
            {fetch_where}
        """

        # 地区权限
        region = ' AND 1=1 '
        if params['region_id'] and isinstance(params['region_id'], list):
            region = '''
                    AND (
                    from_province_id IN (%(region_id)s)
                    OR from_city_id IN (%(region_id)s)
                    OR from_county_id IN (%(region_id)s)
                    OR from_town_id IN (%(region_id)s)
                    ) ''' % {'region_id': ','.join(params['region_id'])}

        fetch_where += region

        # 直接过滤的字段
        svs_list = ('from_province_id', 'from_city_id', 'from_county_id', 'from_town_id',
                    'to_province_id', 'to_city_id', 'to_county_id', 'to_town_id')

        for key, value in params.items():
            if key in svs_list and value and isinstance(value, int):
                fetch_where += ' AND {key} = {value}'.format(key=key, value=value)

        # 特殊条件
        if params.get('special_tag'):
            fetch_where += """
            AND (
                ({special_tag}=1 AND shu_users.create_time > UNIX_TIMESTAMP(DATE(NOW())) AND shu_users.create_time < UNIX_TIMESTAMP()) OR
                ({special_tag}=2 AND ( SELECT COUNT( 1 ) FROM shf_goods WHERE user_id = shu_users.id ) > 0) OR
                ({special_tag}=3 AND ( SELECT COUNT(1) FROM shb_orders WHERE owner_id = shu_users.id AND `status` = 3) > 0) OR
                ({special_tag}=4 AND ( SELECT COUNT(1) FROM shb_orders WHERE owner_id = shu_users.id AND `status` = 3) = 0) 
                )
            """.format(special_tag=params['special_tag'])

        # 根据注册时间
        if params.get('register_start_time') and params.get('register_end_time'):
            fetch_where += """
                AND shu_users.create_time > {0}
                AND	shu_users.create_time <= {1}
                """.format(params['register_start_time'], params['register_end_time'])

        # 根据记录生成时间
        if params.get('record_start_time') and params.get('record_end_time'):
            fetch_where += """
                AND shf_ltl_pre_goods.create_time > {0}
                AND shf_ltl_pre_goods.create_time <= {1}
                """.format(params['record_start_time'], params['record_end_time'])

        count = cursor.query_one(command.format(fields='COUNT(1) AS count', fetch_where=fetch_where))['count']

        command += 'ORDER BY shf_ltl_pre_goods.id DESC LIMIT %s, %s' % ((page - 1) * limit, limit)

        ltl_data = cursor.query(command.format(fields=fields, fetch_where=fetch_where))

        data = {
            'potential_data': ltl_data if ltl_data else [],
            'count': count if count else 0
        }

        return data
