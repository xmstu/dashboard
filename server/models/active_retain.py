class ActiveUserStatisticModel(object):

    @staticmethod
    def get_active_user_statistic(read_db, read_bi, params):

        fetch_where = """ 1=1 """

        command = """
        SELECT
            FROM_UNIXTIME( tiul.last_login_time, "%Y-%m-%d" ) AS create_time,
            COUNT( DISTINCT tiul.user_id ) AS count 
        FROM
            tb_inf_user_login AS tiul
        WHERE
            {fetch_where}
            AND tiul.last_login_time >= {start_time}
            AND tiul.last_login_time < {end_time}
        """

        # 地区选择
        if params['region_id']:
            if isinstance(params['region_id'], int):
                fetch_where += """
                AND user_id IN (
                SELECT user_id FROM tb_inf_user WHERE 
                from_province_id = %(region_id)s OR 
                from_city_id = %(region_id)s OR
                from_county_id = %(region_id)s OR
                from_town_id = %(region_id)s
                )
                """ % {"region_id": params["region_id"]}
            elif isinstance(params['region_id'], list):
                fetch_where += '''
                        AND user_id IN (
                        SELECT user_id FROM tb_inf_user WHERE 
                        from_province_id IN (%(region_id)s
                        OR from_city_id IN (%(region_id)s
                        OR from_county_id IN (%(region_id)s
                        OR from_town_id IN (%(region_id)s
                        ) ''' % {'region_id': ','.join(params['region_id'])}

        # 用户类型
        if params["user_type"]:
            fetch_where += """
            AND (
            ({user_type}=1 AND user_id IN (SELECT user_id FROM tb_inf_user WHERE is_deleted = 0 AND user_type = 1) ) OR
            ({user_type}=2 AND user_id IN (SELECT user_id FROM tb_inf_user WHERE is_deleted = 0 AND user_type = 2) ) OR
            ({user_type}=3 AND user_id IN (SELECT user_id FROM tb_inf_user WHERE is_deleted = 0 AND user_type = 3) )
            )
            """.format(user_type=params["user_type"])

        # 特殊标签
        if params["special_tag"]:

            sql = """
            SELECT
                id 
            FROM
                shu_users
            WHERE
                is_deleted = 0
                AND create_time >= :start_time
                AND create_time < :end_time
            """

            new_register_user = read_db.query(sql, params)

            new_register_user_id_str = ",".join((str(detail["id"]) for detail in new_register_user))

            new_register_user_id_str = new_register_user_id_str if new_register_user_id_str else -1

            fetch_where += """
            AND (
            {special_tag} = 1 AND user_id NOT IN (
            {new_register_user_id_str}
            )
            )
            """.format(special_tag=params["special_tag"], new_register_user_id_str=new_register_user_id_str)

        # 日/周/月 模式
        if params["periods"] == 2:
            command += """ GROUP BY FROM_UNIXTIME( tiul.last_login_time, "%%%%Y-%%%%m-%%%%d" ) """
        elif params["periods"] == 3:
            command += """ GROUP BY FROM_UNIXTIME( tiul.last_login_time, "%%%%Y%%%%u" ) """
        elif params["periods"] == 4:
            command += """ GROUP BY FROM_UNIXTIME( tiul.last_login_time, "%%%%Y-%%%%m" ) """
        else:
            return []

        data = read_bi.query(command.format(fetch_where=fetch_where, start_time=params["start_time"], end_time=params["end_time"]))

        return data if data else []
