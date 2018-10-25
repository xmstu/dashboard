import datetime
import time


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
            command += """ GROUP BY FROM_UNIXTIME( tiul.last_login_time, "%Y-%m-%d" ) """
        elif params["periods"] == 3:
            command += """ GROUP BY FROM_UNIXTIME( tiul.last_login_time, "%Y%u" ) """
        elif params["periods"] == 4:
            command += """ GROUP BY FROM_UNIXTIME( tiul.last_login_time, "%Y-%m" ) """
        else:
            return []

        data = read_bi.query(command.format(fetch_where=fetch_where, start_time=params["start_time"], end_time=params["end_time"]))

        return data if data else []

    @staticmethod
    def get_active_user_login_list(cursor, params):

        fetch_where = """ 1=1 """

        command = """
        SELECT
            *
        FROM
        (
        SELECT
            "{date_str}" AS active_retain_date,
            COUNT(1) AS first_day_login_count
        FROM
            tb_inf_user
        WHERE
            {fetch_where}
            AND create_time >= UNIX_TIMESTAMP("{date_str}")
            AND create_time < UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 1 DAY))
        ) AS a,
        (
        SELECT
            COUNT(1) AS second_day_login_count
        FROM
            tb_inf_user_login
        WHERE 
            user_id IN (SELECT user_id FROM tb_inf_user WHERE {fetch_where} AND create_time >= UNIX_TIMESTAMP("{date_str}") AND create_time < UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 1 DAY)))
            AND last_login_time >= UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 1 DAY))
            AND last_login_time < UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 2 DAY))
        ) AS b,
        (
        SELECT
            COUNT(1) AS third_day_login_count
        FROM
            tb_inf_user_login
        WHERE 
            user_id IN (SELECT user_id FROM tb_inf_user WHERE {fetch_where} AND create_time >= UNIX_TIMESTAMP("{date_str}") AND create_time < UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 1 DAY)))
            AND last_login_time >= UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 2 DAY))
            AND last_login_time < UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 3 DAY))
        ) AS c,
        (
        SELECT
            COUNT(1) AS fourth_day_login_count
        FROM
            tb_inf_user_login
        WHERE 
            user_id IN (SELECT user_id FROM tb_inf_user WHERE {fetch_where} AND create_time >= UNIX_TIMESTAMP("{date_str}") AND create_time < UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 1 DAY)))
            AND last_login_time >= UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 3 DAY))
            AND last_login_time < UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 4 DAY))
        ) AS d,
        (
        SELECT
            COUNT(1) AS fifth_day_login_count
        FROM
            tb_inf_user_login
        WHERE 
            user_id IN (SELECT user_id FROM tb_inf_user WHERE {fetch_where} AND create_time >= UNIX_TIMESTAMP("{date_str}") AND create_time < UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 1 DAY)))
            AND last_login_time >= UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 4 DAY))
            AND last_login_time < UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 5 DAY))
        ) AS e,
        (
        SELECT
            COUNT(1) AS sixth_day_login_count
        FROM
            tb_inf_user_login
        WHERE 
            user_id IN (SELECT user_id FROM tb_inf_user WHERE {fetch_where} AND create_time >= UNIX_TIMESTAMP("{date_str}") AND create_time < UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 1 DAY)))
            AND last_login_time >= UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 5 DAY))
            AND last_login_time < UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 6 DAY))
        ) AS f,
        (
        SELECT
            COUNT(1) AS seventh_day_login_count
        FROM
            tb_inf_user_login
        WHERE 
            user_id IN (SELECT user_id FROM tb_inf_user WHERE {fetch_where} AND create_time >= UNIX_TIMESTAMP("{date_str}") AND create_time < UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 1 DAY)))
            AND last_login_time >= UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 6 DAY))
            AND last_login_time < UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 7 DAY))
        ) AS g,
        (
        SELECT
            COUNT(1) AS eighth_day_login_count
        FROM
            tb_inf_user_login
        WHERE 
            user_id IN (SELECT user_id FROM tb_inf_user WHERE {fetch_where} AND create_time >= UNIX_TIMESTAMP("{date_str}") AND create_time < UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 1 DAY)))
            AND last_login_time >= UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 7 DAY))
            AND last_login_time < UNIX_TIMESTAMP(DATE_ADD("{date_str}",INTERVAL 8 DAY))
        ) AS h;
        """
        # 权限地区内的用户登录数
        if params.get("region_id"):
            fetch_where += """
            AND from_city_id = {}
            """.format(params["region_id"])

        # 用户类型
        if params.get("user_type"):
            fetch_where += """
            AND (
            ({user_type}=1 AND user_type=1) OR
            ({user_type}=2 AND user_type=2) OR
            ({user_type}=3 AND user_type=3) 
            )
            """.format(user_type=params["user_type"])

        data = []
        date_val = params.pop("start_date")
        end_date = params.pop("end_date")
        while date_val <= end_date:
            date_str = date_val.strftime("%Y-%m-%d")
            date_val += datetime.timedelta(days=1)
            daily_data = cursor.query(command.format(fetch_where=fetch_where, date_str=date_str))
            data += daily_data

        return data

    @staticmethod
    def get_active_consignor_list(cursor, params):

        fields = """"""

        which_table = """"""

        fetch_where = """"""

        command = """"""

        data = cursor.query(command)

        return data

    @staticmethod
    def get_active_driver_list(cursor, params):

        fields = """"""

        which_table = """"""

        fetch_where = """"""

        command = """"""

        data = cursor.query(command)

        return data
