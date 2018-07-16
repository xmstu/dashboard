import time

from server.utils.constant import vehicle_id_name, vehicle_name


class HeatMapModel(object):

    @staticmethod
    def get_user(cursor, params, region_level):

        fetch_where = """ 1=1 """

        command = """
        SELECT
            {region_group},
            COUNT( 1 ) count
        FROM
            `tb_inf_user` 
        WHERE
            {fetch_where} 
            AND create_time < :end_time
            AND is_deleted = 0
            GROUP BY
              {region_group}
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
            # 求新增用户总数
            if params['field'] == 1:
                fetch_where += """ AND create_time >= :start_time  """
            # 求累计用户总数
            elif params['field'] == 2:
                pass
            # 求角色对应的累计认证数
            elif params['field'] == 3:
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
            # 求累计活跃数
            elif params['field'] == 4:
                fetch_where += """
                AND last_login_time < :end_time
                """

        # 根据级别分组数据
        if region_level == 0:
            group_condition = 'from_province_id'
            region_group = 'from_province_id'
        elif region_level == 1:
            group_condition = 'from_province_id'
            region_group = 'from_city_id'
        elif region_level == 2:
            group_condition = 'from_city_id'
            region_group = 'from_county_id'
        elif region_level == 3:
            group_condition = 'from_county_id'
            region_group = 'from_town_id'
        else:
            group_condition = ''
            region_group = ''

        # 根据地区id获取数据
        if int(params.get('region_id')):
            fetch_where += """ AND {group_condition} = {region_id} """.format(group_condition=group_condition, region_id=params['region_id'])

        fetch_where += """ AND {group_condition} != 0 AND {region_group} != 0 """.format(group_condition=group_condition, region_group=region_group)

        kwargs = {
            "start_time": params.get('start_time', time.time() - 86400*7),
            "end_time": params.get('end_time', time.time() - 86400)
        }

        user_list = cursor.query(command.format(fetch_where=fetch_where, region_group=region_group), kwargs)

        data = {
            "user_list": user_list if user_list else [],
            "region_group": region_group
        }

        return data

    @staticmethod
    def get_goods(cursor, params, region_level):

        fetch_where = """ 1=1 """

        command = """
        SELECT
            sg.{region_group},
            IF({field}=1, COUNT( 1 ), 0) goods_count,
            IF({field}=2, COALESCE ( SUM( price_expect + price_addition ), 0 ), 0) goods_price,
            IF({field}=3, COUNT( so.id ), 0) orders_count,
            IF({field}=4, COALESCE ( SUM( so.price ), 0 ), 0) orders_price
        FROM
            shf_goods sg
            LEFT JOIN shb_orders so ON so.goods_id = sg.id 
        WHERE
            {fetch_where}
            AND sg.is_deleted = 0 AND so.is_deleted = 0 AND so.`status` != -1
            AND sg.create_time >= :start_time
            AND sg.create_time <  :end_time
        GROUP BY
            sg.{region_group};
        """

        # 按业务类型分
        if params.get('filter') == 1:
            fetch_where += """
            AND (
            ({filter}=1 AND haul_dist = 1) OR
            ({filter}=2 AND haul_dist = 2)
            )
            """.format(filter=params['filter'])

        # 根据级别分组数据
        if region_level == 0:
            group_condition = 'from_province_id'
            region_group = 'from_province_id'
        elif region_level == 1:
            group_condition = 'from_province_id'
            region_group = 'from_city_id'
        elif region_level == 2:
            group_condition = 'from_city_id'
            region_group = 'from_county_id'
        elif region_level == 3:
            group_condition = 'from_county_id'
            region_group = 'from_town_id'
        else:
            group_condition = ''
            region_group = ''

        # 根据地区id获取数据
        if int(params.get('region_id')):
            fetch_where += """ AND sg.{group_condition} = {region_id} """.format(group_condition=group_condition, region_id=params['region_id'])

        fetch_where += """ AND sg.{group_condition} != 0 AND sg.{region_group} != 0 """.format(group_condition=group_condition, region_group=region_group)

        # 时间
        kwargs = {
            "start_time": params.get("start_time", time.time() - 86400*7),
            "end_time": params.get("end_time", time.time())
        }

        goods_list = cursor.query(command.format(region_group=region_group, field=params['field'], fetch_where=fetch_where), kwargs)

        data = {
            "goods_list": goods_list if goods_list else [],
            "region_group": region_group
        }

        return data

    @staticmethod
    def get_vehicle(cursor1, cursor2, params, region_level):

        fetch_where1 = """ 1=1 """
        fetch_where2 = """ 1=1 """

        cmd1 = """
        SELECT
            shf_goods.{region_group},
            IF({field}=1, COUNT( shf_goods.id ), 0) goods_vehicle_count,
            IF({field}=3, COUNT( shb_orders.id ), 0) order_vehicle_count 
        FROM
            shf_goods
            LEFT JOIN shf_goods_vehicles ON shf_goods_vehicles.goods_id = shf_goods.id
            LEFT JOIN shb_orders ON shb_orders.goods_id = shf_goods_vehicles.goods_id 
        WHERE
            {fetch_where1}
            AND shf_goods.is_deleted = 0 
            AND shb_orders.is_deleted = 0 AND shb_orders.`status` != -1
            AND shf_goods.create_time >= :start_time 
            AND shf_goods.create_time < :end_time 
        GROUP BY
            shf_goods.{region_group}
        """

        cmd2 = """
        SELECT
            vehicle.{region_group},
            IF({field}=2, COUNT( 1 ), 0) vehicle_count
        FROM
            `tb_inf_transport_vehicles` vehicle
            LEFT JOIN tb_inf_user user USING(user_id)
            WHERE
            {fetch_where2}
            AND user.last_login_time >= :start_time 
            AND user.last_login_time < :end_time
            AND vehicle.create_time >= FROM_UNIXTIME(:start_time)
            AND vehicle.create_time < FROM_UNIXTIME(:end_time)
            AND vehicle.vehicle_length_id != ''
        GROUP BY
            vehicle.{region_group};
        """

        # 车长
        if params.get('filter'):
            f = str(params.get('filter'))
            fetch_where1 += """ AND shf_goods_vehicles.`name` = '%s' """ % vehicle_name.get(f, '小面包车')
            fetch_where2 += """ AND vehicle.vehicle_length_id LIKE "%%%s%%"  """ % vehicle_id_name.get(vehicle_name.get(f, '小面包车'), '')

        # 根据级别分组数据
        if region_level == 0:
            group_condition = 'from_province_id'
            region_group = 'from_province_id'
        elif region_level == 1:
            group_condition = 'from_province_id'
            region_group = 'from_city_id'
        elif region_level == 2:
            group_condition = 'from_city_id'
            region_group = 'from_county_id'
        elif region_level == 3:
            group_condition = 'from_county_id'
            region_group = 'from_town_id'
        else:
            group_condition = ''
            region_group = ''

        # 根据地区id获取数据
        if int(params.get('region_id')):
            fetch_where1 += """ AND shf_goods.{group_condition} = {region_id} """.format(group_condition=group_condition, region_id=params['region_id'])
            fetch_where2 += """ AND vehicle.{group_condition} = {region_id} """.format(group_condition=group_condition, region_id=params['region_id'])

        fetch_where1 += """ AND shf_goods.{group_condition} != 0 AND shf_goods.{region_group} != 0 """.format(group_condition=group_condition, region_group=region_group)
        fetch_where2 += """ AND vehicle.{group_condition} != 0 AND vehicle.{region_group} != 0 """.format(group_condition=group_condition, region_group=region_group)

        # 时间
        kwargs = {
            "start_time": params.get("start_time", time.time() - 86400 * 7),
            "end_time": params.get("end_time", time.time())
        }

        ret1 = cursor1.query(cmd1.format(region_group=region_group, field=params.get('field', 1), fetch_where1=fetch_where1), kwargs)
        ret2 = cursor2.query(cmd2.format(region_group=region_group, field=params.get('field', 1), fetch_where2=fetch_where2), kwargs)

        for i in ret1:
            vehicle_count = [j['vehicle_count'] for j in ret2 if j[region_group] == i[region_group]]
            if vehicle_count:
                i['vehicle_count'] = vehicle_count[0]
            else:
                i['vehicle_count'] = 0

        data = {
            'vehicle_list': ret1 if ret1 else [],
            'region_group': region_group,
        }

        return data
