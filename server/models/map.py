import time

from server.cache_data import init_regions
from server.utils.calc_dstance import calcDistance
from server.utils.constant import vehicle_name_id


class DistributionMapModel(object):

    @staticmethod
    def get_user(cursor, params, region_level):

        fetch_where = """ 1=1 """
        table = """ `tb_inf_user` """

        command = """
        SELECT
            {region_group},
            COUNT( 1 ) count
        FROM
            {table}
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
            ( {filter}=0) OR
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
            # 统计时间内登陆过
            elif params['field'] == 4:
                fetch_where += """
                AND last_login_time >= :start_time
                AND last_login_time < :end_time
                """
            # 均有登录
            elif params['field'] == 5:
                table += """ LEFT JOIN tb_inf_user_login login USING(user_id) """
                fetch_where += """
                AND login.last_login_time > :start_time
                AND login.last_login_time <= :end_time
                AND (SELECT COUNT( 1 ) FROM tb_inf_user_login WHERE user_id = login.user_id AND last_login_time > :start_time AND last_login_time <= :end_time) = :days
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
            fetch_where += """ AND {group_condition} = {region_id} """.format(group_condition=group_condition,
                                                                              region_id=params['region_id'])

        fetch_where += """ AND {group_condition} != 0 AND {region_group} != 0 """.format(
            group_condition=group_condition, region_group=region_group)

        start_time = params.get('start_time', time.time() - 86400 * 7)
        end_time = params.get('end_time', time.time())
        days = int(round((end_time - start_time) / 86400))

        kwargs = {
            "start_time": start_time,
            "end_time": end_time,
            "days": days
        }

        user_list = cursor.query(command.format(table=table, fetch_where=fetch_where, region_group=region_group),
                                 kwargs)

        data = {
            "ret_list": user_list if user_list else [],
            "region_group": region_group
        }

        return data

    @staticmethod
    def get_goods(cursor, params, region_level):

        fetch_where = """ 1=1 """

        command = """
        SELECT
            sg.{region_group},
            COUNT( 1 ) count
        FROM
            shf_goods sg
        WHERE
            {fetch_where}
            AND sg.is_deleted = 0
            AND sg.create_time >= :start_time
            AND sg.create_time <  :end_time
        GROUP BY
            sg.{region_group};
        """

        # 按业务类型分
        if params.get('filter'):
            fetch_where += """
            AND (
            ( {filter}=0) OR
            ({filter}=1 AND sg.is_system_price = 0) OR
            ({filter}=2 AND sg.is_system_price = 1)
            )
            """.format(filter=params['filter'])

        # 按统计方式分 货源数 接单数 取消数 待接单数
        if params.get('field'):
            fetch_where += """
                AND (
                ({field}=1) OR
                ({field}=2 AND sg.status = 3) OR
                ({field}=3 AND sg.status = -1) OR
                ({field}=4 AND sg.status IN (1, 2))
                ) 
                """.format(field=params['field'])

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
            fetch_where += """ AND sg.{group_condition} = {region_id} """.format(group_condition=group_condition,
                                                                                 region_id=params['region_id'])

        fetch_where += """ AND sg.{group_condition} != 0 AND sg.{region_group} != 0 """.format(
            group_condition=group_condition, region_group=region_group)

        # 时间
        kwargs = {
            "start_time": params.get("start_time", time.time() - 86400 * 7),
            "end_time": params.get("end_time", time.time())
        }

        goods_list = cursor.query(
            command.format(region_group=region_group, fetch_where=fetch_where), kwargs)

        data = {
            "ret_list": goods_list if goods_list else [],
            "region_group": region_group
        }

        return data

    @staticmethod
    def get_vehicle(cursor1, cursor2, params, region_level):

        fetch_where1 = """ 1=1 """
        fetch_where2 = """ 1=1 """

        vehicle_table = """ `tb_inf_transport_vehicles` vehicle """

        cmd1 = """
        SELECT
            shf_goods.{region_group},
            COUNT( shf_goods.id ) count
        FROM
            shf_goods
            INNER JOIN shf_goods_vehicles ON shf_goods_vehicles.goods_id = shf_goods.id
        WHERE
            {fetch_where1}
            AND shf_goods.is_deleted = 0 
            AND shf_goods.create_time >= :start_time 
            AND shf_goods.create_time < :end_time 
        GROUP BY
            shf_goods.{region_group}
        """

        cmd2 = """
        SELECT
            vehicle.{region_group},
            COUNT( 1 ) count
        FROM
            {vehicle_table}
        WHERE
            {fetch_where2}
            AND vehicle.create_time < FROM_UNIXTIME(:end_time)
            AND vehicle.vehicle_length_id != ''
        GROUP BY
            vehicle.{region_group};
        """

        # 车长
        if params.get('filter'):
            fetch_where1 += """ AND shf_goods_vehicles.`name` = '%s' """ % params['filter']
            fetch_where2 += """ AND vehicle.vehicle_length_id REGEXP ",{vehicle_id}|{vehicle_id},|,{vehicle_id},|^{vehicle_id}$" """.format(vehicle_id=vehicle_name_id.get(params['filter'], ''))

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
            fetch_where1 += """ AND shf_goods.{group_condition} = {region_id} """.format(
                group_condition=group_condition, region_id=params['region_id'])
            fetch_where2 += """ AND vehicle.{group_condition} = {region_id} """.format(group_condition=group_condition,
                                                                                       region_id=params['region_id'])

        fetch_where1 += """ AND shf_goods.{group_condition} != 0 AND shf_goods.{region_group} != 0 """.format(
            group_condition=group_condition, region_group=region_group)
        fetch_where2 += """ AND vehicle.{group_condition} != 0 AND vehicle.{region_group} != 0 """.format(
            group_condition=group_condition, region_group=region_group)

        # 时间
        kwargs = {
            "start_time": params.get("start_time", time.time() - 86400 * 7),
            "end_time": params.get("end_time", time.time())
        }

        ret = None
        if params.get('field'):
            if params['field'] == 1:
                ret = cursor1.query(cmd1.format(region_group=region_group, fetch_where1=fetch_where1), kwargs)
            elif params['field'] == 2:
                ret = cursor2.query(cmd2.format(vehicle_table=vehicle_table, region_group=region_group, fetch_where2=fetch_where2), kwargs)
            elif params['field'] == 3:
                vehicle_table += """ LEFT JOIN tb_inf_user user USING(user_id) """
                fetch_where2 += """ 
                AND user.last_login_time >= :start_time 
                AND user.last_login_time < :end_time
                AND vehicle.create_time >= FROM_UNIXTIME(:start_time)
                """
                ret = cursor2.query(cmd2.format(vehicle_table=vehicle_table, region_group=region_group, fetch_where2=fetch_where2), kwargs)

        data = {
            'ret_list': ret if ret else [],
            'region_group': region_group,
        }

        return data

    @staticmethod
    def get_order(cursor, params, region_level):
        fetch_where = """ 1=1 """
        command = """
        SELECT
            so.{region_group},
            COUNT(1) count
        FROM
            shb_orders so INNER JOIN shf_goods sg ON sg.id = so.goods_id AND so.is_deleted = 0 AND so.`status` != -1
        WHERE
            {fetch_where}
            AND so.create_time >= :start_time
            AND so.create_time < :end_time
        GROUP BY so.{region_group};
        """

        # 按业务类型分
        if params.get('filter'):
            fetch_where += """
                    AND (
                    ({filter}=0) OR
                    ({filter}=1 AND sg.is_system_price = 0) OR
                    ({filter}=2 AND sg.is_system_price = 1)
                    )
                    """.format(filter=params['filter'])

        # 按统计方式分 订单数 完成数 进行数 已取消数
        if params.get('field'):
            fetch_where += """
                        AND (
                        ({field}=1) OR
                        ({field}=2 AND so.status = 3) OR
                        ({field}=3 AND so.status IN (1, 2)) OR
                        ({field}=4 AND so.status = -1)
                        ) 
                        """.format(field=params['field'])

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
            fetch_where += """ AND so.{group_condition} = {region_id} """.format(group_condition=group_condition,
                                                                                 region_id=params['region_id'])

        fetch_where += """ AND so.{group_condition} != 0 AND so.{region_group} != 0 """.format(
            group_condition=group_condition, region_group=region_group)

        # 时间
        kwargs = {
            "start_time": params.get("start_time", time.time() - 86400 * 7),
            "end_time": params.get("end_time", time.time())
        }

        orders_list = cursor.query(
            command.format(region_group=region_group, fetch_where=fetch_where), kwargs)

        data = {
            "ret_list": orders_list if orders_list else [],
            "region_group": region_group
        }

        return data


class GoodsMapModel(object):

    @staticmethod
    def get_data(cursor, user_id_list, params):

        which_table = """ shf_goods """

        fetch_where = """ 1=1 """

        command = """
        SELECT
            from_latitude AS lat,
            from_longitude AS lng,
            COUNT( 1 ) count 
        FROM
            {which_table}
            -- INNER JOIN shu_users ON shu_users.id = shf_goods.user_id AND is_test = 0
        WHERE
            {fetch_where} 
            AND shf_goods.from_longitude != 0
        GROUP BY
            from_latitude,
            from_longitude;
        """

        # 权限地区
        region = """ AND 1=1 """
        if params.get('role_region_id'):
            region = '''
                    AND (
                    shf_goods.from_province_id IN (%(role_region_id)s)
                    OR shf_goods.from_city_id IN (%(role_region_id)s)
                    OR shf_goods.from_county_id IN (%(role_region_id)s)
                    OR shf_goods.from_town_id IN (%(role_region_id)s)
                    ) ''' % {'role_region_id': ','.join(params['role_region_id'])}

        fetch_where += region

        which_table, fetch_where = GoodsMapModel.complete_fetch_where(params, user_id_list, which_table, fetch_where)
        data = cursor.query(command.format(which_table=which_table, fetch_where=fetch_where))

        if not data:
            return {}, []

        max_data = max(data, key=lambda i: i["count"])
        max_lat_lng = {"max_count": max_data["count"], "max_lat": float(max_data["lat"]), "lng": float(max_data["lng"])}

        for detail in data:
            detail['lat'] = float(detail['lat'])
            detail['lng'] = float(detail['lng'])

        return max_lat_lng if max_lat_lng else {}, data if data else []

    @staticmethod
    def post_data(cursor, user_id_list, params):

        which_table = """ shf_goods """

        fetch_where = """ 1 = 1 """

        command = """
        SELECT
            from_latitude AS lat,
            from_longitude AS lng,
            COUNT( 1 ) count 
        FROM
            {which_table}
        WHERE
            {fetch_where} 
            AND shf_goods.from_longitude != 0 
            AND shf_goods.from_latitude != 0
        GROUP BY
            from_latitude,
            from_longitude
        """

        region_id = params.pop("region_id")
        lat = params.pop("lat")
        lng = params.pop("lng")
        multiple = params.pop("multiple")

        start_lat = lat - 0.008983 * multiple
        end_lat = lat + 0.008983 * multiple
        start_lng = lng - 0.011576 * multiple
        end_lng = lng + 0.011576 * multiple

        level = init_regions.get_current_region_level(region_id)
        if level:
            fetch_where += """
            AND (
            ({level}=1 AND from_province_id={region_id}) OR
            ({level}=2 AND from_city_id={region_id}) OR
            ({level}=3 AND from_county_id={region_id}) OR
            ({level}=4 AND from_town_id={region_id}) 
            )
            """.format(level=level, region_id=region_id)

        which_table, fetch_where = GoodsMapModel.complete_fetch_where(params, user_id_list, which_table, fetch_where)
        data = cursor.query(command.format(which_table=which_table, fetch_where=fetch_where))

        ret = []
        for detail in data:
            if detail["lat"] < start_lat:
                continue
            if detail["lat"] > end_lat:
                continue
            if detail["lng"] < start_lng:
                continue
            if detail["lng"] > end_lng:
                continue
            ret.append(detail["count"])
        if ret:
            sum_count = sum(ret)
            data = {
                "lat": lat,
                "lng": lng,
                "sum_count": sum_count,
            }
        else:
            data = {
                "lat": lat,
                "lng": lng,
                "sum_count": 0,
            }
        return data

    @staticmethod
    def complete_fetch_where(params, user_id_list, which_table, fetch_where):
        # 一口价/议价
        if params.get('goods_price_type'):
            fetch_where += """
                        AND (
                        ({0}=1 AND is_system_price=1) OR
                        ({0}=2 AND is_system_price=0) 
                        )
                        """.format(params['goods_price_type'])

        # 距离
        if params.get('haul_dist'):
            fetch_where += """
                        AND (
                        ({0}=1 AND haul_dist=1) OR
                        ({0}=2 AND haul_dist=2) 
                        )
                        """.format(params['haul_dist'])

        # 车长
        if params.get('vehicle_length'):
            which_table += """ INNER JOIN shf_goods_vehicles ON shf_goods_vehicles.goods_id = shf_goods.id """
            fetch_where += """ AND shf_goods_vehicles.`name` = '{0}' """.format(params['vehicle_length'])

        # 货源状态
        if params.get('goods_status'):
            fetch_where += """
                        AND (
                        ({0}=1 AND shf_goods.`status` IN (1,2)) OR
                        ({0}=2 AND shf_goods.`status` = 3) OR
                        ({0}=3 AND shf_goods.id IN ( SELECT goods_id FROM shb_orders WHERE `status` = 3 )) OR
                        ({0}=4 AND (shf_goods.`status` = -1 OR shf_goods.is_deleted = 0))
                        )
                        """.format(params['goods_status'])

        # 新用户
        if user_id_list:
            fetch_where += """ AND shf_goods.user_id IN (%s) """ % ','.join(user_id_list)

        # 发货时间
        if params['delivery_start_time'] and params['delivery_end_time']:
            fetch_where += """ 
                        AND shf_goods.create_time >= {0} 
                        AND shf_goods.create_time < {1} """.format(params['delivery_start_time'],
                                                                   params['delivery_end_time'])

        # 注册时间
        if params['register_start_time'] and params['register_end_time']:
            which_table += """ INNER JOIN shu_users ON shu_users.id = shf_goods.user_id AND is_test = 0 """
            fetch_where += """ 
                            AND shu_users.create_time >= {0} 
                            AND shu_users.create_time < {1} """.format(params['register_start_time'],
                                                                       params['register_end_time'])

        return which_table, fetch_where


class UsersMapModel(object):

    @staticmethod
    def get_data(cursor, params):

        fields = """"""

        which_table = """"""

        fetch_where = """"""

        command = """"""

        data = cursor.query(command)

        return data
