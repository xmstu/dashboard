from server import log
from server.cache_data import vehicle_id_list, init_regions
from server.utils.constant import vehicle_name_id, vehicle_name_list


class TransportRadarModel(object):

    @staticmethod
    def get_data(read_bi, params):

        vehicle_cmd = """
        SELECT
            {vehicle_count} vehicle_count
        FROM
            `tb_inf_transport_vehicles` vehicle
            INNER JOIN tb_inf_user user USING(user_id)
            WHERE
            {vehicle_sql}
            AND user.driver_auth = 1
            AND UNIX_TIMESTAMP(vehicle.create_time) < :end_time
            AND vehicle.vehicle_length_id != ''
            AND vehicle.vehicle_length_id REGEXP ",{vehicle_id}|{vehicle_id},|,{vehicle_id},|^{vehicle_id}$"
        """

        vehicle_sql = """ 1=1 """

        # 权限地区
        vehicle_region = ' AND 1=1 '
        if params['region_id']:
            if isinstance(params['region_id'], int):
                vehicle_region = """ 
                AND (vehicle.from_province_id = %(region_id)s 
                OR vehicle.from_city_id = %(region_id)s 
                OR vehicle.from_county_id = %(region_id)s 
                OR vehicle.from_town_id = %(region_id)s) """ % {'region_id': params['region_id']}
            elif isinstance(params['region_id'], list):
                vehicle_region = '''
                AND (
                vehicle.from_province_id IN (%(region_id)s)
                OR vehicle.from_city_id IN (%(region_id)s)
                OR vehicle.from_county_id IN (%(region_id)s)
                OR vehicle.from_town_id IN (%(region_id)s)
                ) ''' % {'region_id': ','.join(params['region_id'])}

        vehicle_sql += vehicle_region

        # 出发地
        if params.get('from_city_id'):
            vehicle_sql += """ AND vehicle.from_city_id = %d """ % params.get('from_city_id')

        if params.get('from_county_id'):
            vehicle_sql += """ AND vehicle.from_county_id = %d """ % params.get('from_county_id')

        # 目的地
        if params.get('to_city_id'):
            vehicle_sql += """ AND vehicle.to_city_id = %d """ % params.get('to_city_id')

        if params.get('to_county_id'):
            vehicle_sql += """ AND vehicle.to_county_id = %d """ % params.get('to_county_id')

        kwargs = {
            'start_time': params.get('start_time'),
            'end_time': params.get('end_time')
        }

        # 活跃车辆数
        vehicles_ret = []
        # 累计车辆数(非活跃和活跃)
        vehicles_all_ret = []
        vehicle_all_sql = vehicle_sql + """
         AND UNIX_TIMESTAMP(vehicle.create_time) >= :start_time 
         AND user.last_login_time >= :start_time 
         AND user.last_login_time < :end_time """
        for i in vehicle_id_list:
            try:
                vehicle_all_count = read_bi.query_one(vehicle_cmd.format(vehicle_count="COUNT( DISTINCT user_id )",
                                                                         vehicle_sql=vehicle_sql, vehicle_id=i), kwargs)
                vehicles_all_ret.append(vehicle_all_count['vehicle_count'])

                vehicle_count = read_bi.query_one(vehicle_cmd.format(vehicle_count="COUNT(1)",
                                                                     vehicle_sql=vehicle_all_sql, vehicle_id=i), kwargs)
                vehicles_ret.append(vehicle_count['vehicle_count'])

            except Exception as e:
                log.error('Error:{}'.format(e))
                vehicles_ret.append(0)

        data = {
            'vehicle_name_list': vehicle_name_list,
            'vehicles_ret': vehicles_ret,
            'vehicles_all_ret': vehicles_all_ret,
        }

        return data


class TransportListModel(object):

    @staticmethod
    def get_data(cursor, params):

        group_fields = """
        from_city_id,
        to_city_id
        """

        fields = """
        COUNT( 1 ) AS vehicle_count,
        IFNULL(
        (
        SELECT
            COUNT( DISTINCT shu_vehicles.user_id ) 
        FROM
            shf_booking_settings AS sbs
            INNER JOIN shu_user_stats ON shu_user_stats.user_id = sbs.user_id 
        WHERE
            sbs.id = shf_booking_settings.id 
            AND shu_user_stats.last_login_time >= :start_time
            AND shu_user_stats.last_login_time < :end_time
        ) , 0) AS login_driver_count,
        COUNT( DISTINCT shu_vehicles.user_id ) AS total_driver_count,
        """

        fetch_where = """
        AND 1=1
        """

        group_condition = """
        from_city_id,
        to_city_id
        """

        command = """
        SELECT
            {fields}
        FROM
            shf_booking_settings
            INNER JOIN shu_vehicles ON shf_booking_settings.user_id = shu_vehicles.user_id
            INNER JOIN shu_vehicle_auths ON shu_vehicle_auths.vehicle_id = shu_vehicles.id 
            AND shu_vehicles.is_deleted = 0 
            AND shu_vehicle_auths.auth_status = 2 
            AND shu_vehicle_auths.is_deleted = 0
        WHERE
            shf_booking_settings.is_deleted = 0 
            AND from_city_id = :from_city_id 
            AND to_city_id = :to_city_id 
            AND shf_booking_settings.create_time >= :start_time
            AND shf_booking_settings.create_time < :end_time
            {fetch_where}
        GROUP BY
            {group_condition}
        """
        # 地区权限
        region = ' AND 1=1 '
        if params['region_id'] and isinstance(params['region_id'], list):
            region = '''
                    AND (
                    shf_booking_settings.from_province_id IN (%(region_id)s)
                    OR shf_booking_settings.from_city_id IN (%(region_id)s)
                    OR shf_booking_settings.from_county_id IN (%(region_id)s)
                    OR shf_booking_settings.from_town_id IN (%(region_id)s)
                    ) ''' % {'region_id': ','.join(params['region_id'])}

        fetch_where += region

        # 计算城市概况
        general_situation = cursor.query(command.format(fields=fields+group_fields, fetch_where=fetch_where, group_condition=group_condition), params)

        # 是否计算区镇
        if params["calc_town"] == 1:
            fetch_where += """
            AND from_county_id != 0
            """
            group_fields = group_condition = """
            from_city_id,
            from_county_id,
            to_city_id
            """

        elif params["calc_town"] == 2:
            fetch_where += """
            AND to_county_id != 0
            """
            group_fields = group_condition = """
            from_city_id,
            to_city_id,
            to_county_id
            """

        elif params["calc_town"] == 3:
            fetch_where += """
            AND from_county_id != 0
            AND to_county_id != 0
            """
            group_fields = group_condition = """
            from_city_id,
            from_county_id,
            to_city_id,
            to_county_id
            """

        count = cursor.query(command.format(fields="COUNT(1) AS count", fetch_where=fetch_where, group_condition=group_condition), params)
        count = len(count)

        command += " LIMIT {0}, {1}".format(params["page"], params["limit"])

        transport_list = cursor.query(command.format(fields=fields+group_fields, fetch_where=fetch_where, group_condition=group_condition), params)

        return {"general_situation": general_situation, "count": count if count else 0, "transport_list": transport_list if transport_list else []}
