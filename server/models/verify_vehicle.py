from server.utils.constant import vehicle_name_id


class VerifyVehicleModel(object):

    @staticmethod
    def get_data(cursor, page, limit, params):

        fields = """
            shu_vehicles.id,
            user_name,
            mobile,
            number,
            home_station_province_id,
            home_station_city_id,
            home_station_county_id,
            home_station_town_id,
            type.name type_name,
            length.name length_name,
            IF(shu_vehicle_auths.audit_time, FROM_UNIXTIME(shu_vehicle_auths.audit_time,'%Y-%m-%d'), '') audit_time,
            IF(last_login_time, FROM_UNIXTIME(last_login_time,'%Y-%m-%d'), '') last_login_time
        """

        fetch_where = """1=1"""

        command = """
        SELECT
            {fields}
        FROM
            shu_vehicles
            INNER JOIN shu_vehicle_auths on shu_vehicles.id = shu_vehicle_auths.vehicle_id AND shu_vehicle_auths.auth_status = 2
            LEFT JOIN shu_users on shu_vehicles.user_id = shu_users.id
            LEFT JOIN shu_user_stats USING(user_id)
            LEFT JOIN shu_user_profiles USING(user_id)
            LEFT JOIN shm_dictionary_items type ON type.id = shu_vehicle_auths.type_id
            LEFT JOIN shm_dictionary_items length ON length.id = shu_vehicle_auths.length_id
        WHERE 
            {fetch_where}
            GROUP BY shu_vehicles.id
        """

        # 地区权限
        if params.get('region_id') and isinstance(params.get('region_id'), list):
            fetch_where += """
            AND ( 
            (shu_vehicle_auths.home_station_province_id IN {region_id}) OR
            (shu_vehicle_auths.home_station_city_id IN {region_id}) OR
            (shu_vehicle_auths.home_station_county_id IN {region_id}) OR
            (shu_vehicle_auths.home_station_town_id IN {region_id})
            )
            """.format(region_id=','.join(params['region_id']))

        # 手机号
        if params.get('mobile'):
            fetch_where += """ AND mobile = {0} """.format(params['mobile'])

        # 车牌号码
        if params.get('vehicle_number'):
            fetch_where += """ AND shu_vehicle_auths.number = '{0}' """.format(params['vehicle_number'])

        # 常驻地id
        if params.get('home_station_id'):
            fetch_where += """ 
            AND ( 
            (shu_vehicle_auths.home_station_province_id = {0}) OR
            (shu_vehicle_auths.home_station_city_id = {0}) OR
            (shu_vehicle_auths.home_station_county_id = {0}) OR
            (shu_vehicle_auths.home_station_town_id = {0})
            )
            """.format(params['home_station_id'])

        # 车长要求
        if params.get('vehicle_length'):
            fetch_where += """ AND length_id = {0} """.format(vehicle_name_id.get(params['vehicle_length'], '0'))

        # 认证时间
        if params.get('verify_start_time') and params.get('verify_end_time'):
            fetch_where += """ 
            AND shu_vehicle_auths.audit_time >= {0} AND shu_vehicle_auths.audit_time < {1} 
            """.format(params['verify_start_time'], params['verify_end_time'])

        # 最后登录时间
        if params.get('last_login_start_time') and params.get('last_login_end_time'):
            fetch_where += """ 
            AND last_login_time >= {0} AND last_login_time < {1} 
            """.format(params['last_login_start_time'], params['last_login_end_time'])

        # 计算条数
        ret = cursor.query(command.format(fields='COUNT(*)', fetch_where=fetch_where))
        count = len(ret)

        command += """ DESC LIMIT {0}, {1} """.format((page-1)*limit, limit)

        verify_vehicle_list = cursor.query(command.format(fields=fields, fetch_where=fetch_where))

        data = {
            'count': count if count else 0,
            'verify_vehicle_list': verify_vehicle_list if verify_vehicle_list else []
        }

        return data
