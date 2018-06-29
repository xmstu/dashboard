# -*- coding: utf-8 -*-
import time

from server import log


class GoodsList(object):

    @staticmethod
    def get_goods_list(cursor, page, limit, user_id_list, params):

        fetch_where = """ 1=1 """

        fields = """
                shf_goods.id,
                shf_goods.NAME,
                shf_goods.weight,
                shf_goods.volume,
                shf_goods.type,
                shf_goods.goods_level,
                shf_goods.haul_dist,
                shf_goods.from_province_id,
                shf_goods.from_city_id,
                shf_goods.from_county_id,
                shf_goods.from_town_id,
                shf_goods.to_province_id,
                shf_goods.to_city_id,
                shf_goods.to_county_id,
                shf_goods.to_town_id,
                shf_goods.from_address,
                shf_goods.to_address,
                shf_goods.mileage_total,
                shf_goods.STATUS,
                CASE WHEN
                ((shf_goods.loading_time_is_realtime = 1 AND (UNIX_TIMESTAMP() - shf_goods.create_time) > 600)
                OR (shf_goods.loading_time_is_realtime = 0 
                AND ((UNIX_TIMESTAMP() - shf_goods.loading_time_period_begin)>0 
                OR (UNIX_TIMESTAMP() - UNIX_TIMESTAMP(shf_goods.loading_time_date))>0))) THEN 1 ELSE 0 END AS expire,
                -- 旧车型
                (SELECT IF(shf_goods_vehicles.attribute_value_id = 0, '不限车型', GROUP_CONCAT(shm_dictionary_items.`name`))
                FROM shf_goods_vehicles
                LEFT JOIN shm_dictionary_items ON shf_goods_vehicles.attribute_value_id = shm_dictionary_items.id AND shm_dictionary_items.is_deleted = 0
                WHERE shf_goods_vehicles.goods_id = shf_goods.id AND shf_goods_vehicles.vehicle_attribute = 1
                AND shf_goods_vehicles.is_deleted = 0
                ) AS vehicle_type,
                -- 新车型
                shf_goods_vehicles.`name` AS new_vehicle_type,
                shf_goods.price_recommend,
                shf_goods.price_expect,
                shf_goods.price_addition,
                shu_users.mobile,
                ( SELECT COUNT( 1 ) FROM shf_goods WHERE user_id = shu_users.id ) AS shf_goods_counts,
                (
                SELECT
                    COUNT( 1 ) 
                FROM
                    shu_call_records 
                WHERE
                    source_type = 1 
                    AND source_id = shf_goods.id 
                    AND ( owner_id = shf_goods.user_id OR user_id = shf_goods.user_id ) 
                ) AS call_count,
                shf_goods.create_time,
                (
                SELECT
                    MIN( shu_call_records.start_time ) 
                FROM
                    shu_call_records 
                WHERE
                    shu_call_records.source_type = 1 
                    AND shu_call_records.user_id = shf_goods.user_id 
                    AND shu_call_records.source_id = shf_goods.id 
                ) AS called_time,
                FROM_UNIXTIME( shf_goods.create_time, '%Y-%m-%d %H:%I:%S' ) AS shf_goods_create_time,
                -- 旧版装货时间
                shf_goods.loading_time_date,
                shf_goods.loading_time_period,
                -- 新版装货时间
                shf_goods.loading_time_period_begin,
                shf_goods_vehicles.need_open_top,
                shf_goods_vehicles.need_tail_board,
                shf_goods_vehicles.need_flatbed,
                shf_goods_vehicles.need_high_sided,
                shf_goods_vehicles.need_box,
                shf_goods_vehicles.need_steel,
                shf_goods_vehicles.need_double_seat,
                shf_goods_vehicles.need_remove_seat
        """

        command = """
                    SELECT 
                    {fields}
                    FROM shf_goods
                    LEFT JOIN shu_users ON shf_goods.user_id = shu_users.id
                    LEFT JOIN shf_goods_vehicles ON shf_goods_vehicles.goods_id = shf_goods.id
                    AND shf_goods_vehicles.vehicle_attribute = 3 AND shf_goods_vehicles.is_deleted = 0
                    WHERE {fetch_where}
        """

        # 地区
        region = ' AND 1=1 '
        if params['node_id']:
            if isinstance(params['node_id'], int):
                region = 'AND (from_province_id = %(region_id)s OR from_city_id = %(region_id)s OR from_county_id = %(region_id)s OR from_town_id = %(region_id)s) ' % {
                    'region_id': params['node_id']}
            elif isinstance(params['node_id'], list):
                region = '''
                        AND (
                        from_province_id IN (%(region_id)s)
                        OR from_city_id IN (%(region_id)s)
                        OR from_county_id IN (%(region_id)s)
                        OR from_town_id IN (%(region_id)s)
                        ) ''' % {'region_id': ','.join(params['node_id'])}

        fetch_where += region

        # 货源id
        if params['goods_id']:
            fetch_where += ' AND shf_goods.id = %s AND shf_goods.is_deleted = 0 ' % params['goods_id']

        # 手机
        if params['mobile']:
            fetch_where += ' AND shu_users.mobile = "%s" ' % params['mobile']

        # 出发地
        if params['from_county_id']:
            fetch_where += ' AND shf_goods.from_county_id = %s ' % params['from_county_id']
        if params['from_city_id']:
            fetch_where += ' AND shf_goods.from_city_id = %s ' % params['from_city_id']
        if params['from_province_id']:
            fetch_where += ' AND shf_goods.from_province_id = %s ' % params['from_province_id']

        # 目的地
        if params['to_county_id']:
            fetch_where += ' AND shf_goods.to_county_id = %s ' % params['to_county_id']
        if params['to_city_id']:
            fetch_where += ' AND shf_goods.to_city_id = %s ' % params['to_city_id']
        if params['to_province_id']:
            fetch_where += ' AND shf_goods.to_province_id = %s ' % params['to_province_id']

        # 货源类型
        if params['goods_type']:
            fetch_where += """
                AND(
                ( {goods_type}=1 AND shf_goods.haul_dist = 1 AND shf_goods.type = 1) OR
                ( {goods_type}=2 AND shf_goods.haul_dist = 2 AND shf_goods.goods_level = 2 AND shf_goods.type = 1) OR
                ( {goods_type}=3 AND shf_goods.haul_dist = 2 AND shf_goods.goods_level = 1 AND shf_goods.type = 1) OR
                ( {goods_type}=4 AND shf_goods.type = 2)
                )
            """.format(goods_type=params['goods_type'])

        # 货源状态
        if params['goods_status']:
            if params['goods_status'] == 1:
                fetch_where += ' AND shf_goods.status IN (1,2) AND shf_goods.expired_timestamp < UNIX_TIMESTAMP() '
            if params['goods_status'] == 2:
                fetch_where += ' AND shf_goods.status = 3 AND shf_goods.expired_timestamp < UNIX_TIMESTAMP() '
            if params['goods_status'] == 3:
                fetch_where += ' AND shf_goods.status = -1 AND shf_goods.expired_timestamp < UNIX_TIMESTAMP() '
            if params['goods_status'] == 4:
                fetch_where += """ AND shf_goods.status IN (1, 2)
                                AND ((shf_goods.loading_time_is_realtime = 1 AND (UNIX_TIMESTAMP() - shf_goods.create_time) > 600)
                                OR (shf_goods.loading_time_is_realtime = 0 
                                AND ((UNIX_TIMESTAMP() - shf_goods.loading_time_period_end)>0 
                                OR (UNIX_TIMESTAMP() - UNIX_TIMESTAMP(shf_goods.loading_time_date))>0))) """

        # 是否通话
        if params['is_called']:
            called_sql = """ AND (SELECT COUNT(1)
                            FROM shu_call_records
                            WHERE source_type = 1
                            AND source_id = shf_goods.id
                            AND (owner_id = shf_goods.user_id OR user_id = shf_goods.user_id)) """
            if params['is_called'] == 1:
                fetch_where += called_sql + '> 0 '
            if params['is_called'] == 2:
                fetch_where += called_sql + '= 0 '

        # 车长要求
        if params['vehicle_length']:
            fetch_where += """ AND shf_goods_vehicles.name = '%s' """ % params['vehicle_length']

        # 车型要求
        if params.get('vehicle_type'):
            fetch_where += """
            AND (
            ( {vehicle_type}=1 AND shf_goods_vehicles.need_open_top = 1) OR
            ( {vehicle_type}=2 AND shf_goods_vehicles.need_tail_board = 1) OR
            ( {vehicle_type}=3 AND shf_goods_vehicles.need_flatbed = 1) OR
            ( {vehicle_type}=4 AND shf_goods_vehicles.need_high_sided = 1) OR
            ( {vehicle_type}=5 AND shf_goods_vehicles.need_box = 1) OR
            ( {vehicle_type}=6 AND shf_goods_vehicles.need_steel = 1) OR
            ( {vehicle_type}=7 AND shf_goods_vehicles.need_double_seat = 1) OR
            ( {vehicle_type}=8 AND shf_goods_vehicles.need_remove_seat = 1) 
            )
            """.format(vehicle_type=params['vehicle_type'])

        # 是否初次下单
        if params['new_goods_type'] == 1:
            fetch_where += """ AND shf_goods.user_id IN (%s) """ % ','.join(user_id_list)

        # 急需处理
        if params['urgent_goods']:
            if params['urgent_goods'] == 1:
                fetch_where += """ AND (UNIX_TIMESTAMP() - shf_goods.create_time) > 0 AND (UNIX_TIMESTAMP() - shf_goods.create_time) < 300 """
            if params['urgent_goods'] == 2:
                fetch_where += """ AND (UNIX_TIMESTAMP() - shf_goods.create_time) >= 300 AND (UNIX_TIMESTAMP() - shf_goods.create_time) <= 600 """
            if params['urgent_goods'] == 3:
                fetch_where += """ AND (UNIX_TIMESTAMP() - shf_goods.create_time) > 600 """

        # 是否加价
        if params['is_addition']:
            if params['is_addition'] == 1:
                fetch_where += ' AND shf_goods.price_addition > 0 '
            elif params['is_addition'] == 2:
                fetch_where += ' AND shf_goods.price_addition = 0 '

        # 发布时间
        if params['create_start_time'] and params['create_end_time']:
            fetch_where += """ AND shf_goods.create_time >= %s AND shf_goods.create_time < %s """ % (
                params['create_start_time'], params['create_end_time'])

        # 装货时间
        if params['load_start_time'] and params['load_end_time']:
            loading_time_date = time.strftime('%Y-%m-%d', time.localtime(params['load_start_time']))
            fetch_where += """ AND ( shf_goods.loading_time_date = '{0}'
            OR -- 新版
            ( shf_goods.loading_time_period_begin >= {1} AND shf_goods.loading_time_period_begin < {2} )) """.format(
            loading_time_date, params['load_start_time'], params['load_end_time'])

        # 优化初次加载速度
        fields_value = list(filter(lambda x: x, [params[i] for i in params]))
        if not fields_value:
            goods_count = cursor.query_one('SELECT COUNT(1) AS goods_count FROM shf_goods WHERE 1=1')['goods_count']
        else:
            goods_count = cursor.query_one(command.format(fields=" COUNT(1) AS goods_count ", fetch_where=fetch_where))['goods_count']

        fetch_where += """ ORDER BY shf_goods.id DESC LIMIT %s, %s """ % ((page - 1) * limit, limit)

        goods_detail = cursor.query(command.format(fields=fields, fetch_where=fetch_where))

        goods_list = {'goods_detail': goods_detail if goods_detail else [],
                      'goods_count': goods_count if goods_count else 0}

        return goods_list


class FreshConsignor(object):

    @staticmethod
    def get_user_id_list(cursor, node_id):
        try:
            # 先找出所有下单少于三次的用户id的结果集
            sql = """
                    SELECT
                        user_id 
                    FROM
                        shf_goods 
                    WHERE
                        user_id IN (
                        SELECT DISTINCT
                            user_id 
                        FROM
                            shf_goods 
                        WHERE
                            {region}
                        ) 
                    GROUP BY
                        user_id 
                    HAVING
                        COUNT( * ) < 3;
                    """
            # 地区
            region = ' 1=1 '
            if node_id:
                if isinstance(node_id, int):
                    region += 'AND (from_province_id = %(region_id)s OR from_city_id = %(region_id)s OR from_county_id = %(region_id)s OR from_town_id = %(region_id)s) ' % {
                        'region_id': node_id}
                elif isinstance(node_id, list):
                    region += '''
                            AND (
                            from_province_id IN (%(region_id)s)
                            OR from_city_id IN (%(region_id)s)
                            OR from_county_id IN (%(region_id)s)
                            OR from_town_id IN (%(region_id)s)
                            ) ''' % {'region_id': ','.join(node_id)}
            ret = cursor.query(sql.format(region=region))
            user_id_list = [str(i['user_id']) for i in ret]
            return user_id_list
        except Exception as e:
            log.error('Error:{}'.format(e))
            return ['0']


class CancelReasonList(object):

    @staticmethod
    def get_cancel_reason_list(cursor, params):
        fetch_where = """ 1=1 """

        command = """
        SELECT
            canceled_reason_text,
            COUNT(1) as reason_count
        FROM
            shf_goods 
        WHERE
            canceled_reason_text != ''
            AND ( shf_goods.is_deleted = 1 OR shf_goods.STATUS = - 1 ) 
            AND {fetch_where}
        GROUP BY
            canceled_reason_text
        """

        # 地区
        region = ' AND 1=1 '
        if params['region_id']:
            if isinstance(params['region_id'], int):
                region = 'AND (from_province_id = %(region_id)s OR from_city_id = %(region_id)s OR from_county_id = %(region_id)s OR from_town_id = %(region_id)s) ' % {
                    'region_id': params['region_id']}
            elif isinstance(params['region_id'], list):
                region = '''
                        AND (
                        from_province_id IN (%(region_id)s)
                        OR from_city_id IN (%(region_id)s)
                        OR from_county_id IN (%(region_id)s)
                        OR from_town_id IN (%(region_id)s)
                        ) ''' % {'region_id': ','.join(params['region_id'])}

        fetch_where += region

        # 日期
        if params.get('start_time', 0) and params.get('end_time', 0):
            fetch_where += """ AND create_time >= {start_time} AND create_time < {end_time} """.format(
                start_time=params['start_time'], end_time=params['end_time'])

        # 货源类型
        if params.get('goods_type'):
            fetch_where += """ 
                    AND (({goods_type} = 0) OR
                    -- 同城
                    ({goods_type} = 1 AND haul_dist = 1) OR
                    -- 跨城
                    ({goods_type} = 2 AND haul_dist = 2)) """.format(goods_type=params['goods_type'])

        cancel_list_dict = cursor.query(command.format(fetch_where=fetch_where))

        sum_count = 0
        cancel_list = []
        for i in cancel_list_dict:
            sum_count += i.get('reason_count', None) or 0
            cancel_list.append(list(i.values()))

        for i in cancel_list_dict:
            i.setdefault('percentage', '%.2f%%' % ((i.get('reason_count') / sum_count) * 100))

        data = {
            'cancel_list': cancel_list,
            'cancel_list_dict':cancel_list_dict
        }

        return data


class GoodsDistributionTrendList(object):

    @staticmethod
    def get_goods_distribution_trend(cursor, params):

        fetch_where = """ 1=1 """

        command = """
            SELECT
                FROM_UNIXTIME(create_time, '%Y-%m-%d') AS create_time,
                IF ({flag}, COUNT( DISTINCT user_id ), 0) AS goods_user_count,
                COUNT( 1 ) AS count
            FROM
                shf_goods 
            WHERE
                {fetch_where}
            GROUP BY
                FROM_UNIXTIME(create_time, '%Y-%m-%d')
"""

        # 地区
        region = ' AND 1=1 '
        if params['region_id']:
            if isinstance(params['region_id'], int):
                region = 'AND (from_province_id = %(region_id)s OR from_city_id = %(region_id)s OR from_county_id = %(region_id)s OR from_town_id = %(region_id)s) ' % {
                    'region_id': params['region_id']}
            elif isinstance(params['region_id'], list):
                region = '''
                        AND (
                        from_province_id IN (%(region_id)s)
                        OR from_city_id IN (%(region_id)s)
                        OR from_county_id IN (%(region_id)s)
                        OR from_town_id IN (%(region_id)s)
                        ) ''' % {'region_id': ','.join(params['region_id'])}

        fetch_where += region

        # 日期
        if params.get('start_time', 0) and params.get('end_time', 0):
            fetch_where += """ AND create_time >= {start_time} AND create_time < {end_time} """.format(
                start_time=params['start_time'], end_time=params['end_time'])

        # 货源类型
        if params.get('goods_type'):
            fetch_where += """ 
            AND (({goods_type} = 0) OR
            -- 同城
            ({goods_type} = 1 AND haul_dist = 1) OR
            -- 跨城
            ({goods_type} = 2 AND haul_dist = 2) OR
            -- 零担
            ({goods_type} = 3 AND type = 2)) """.format(goods_type=params['goods_type'])

        wait_where = """ AND ( status = 1 OR status = 2 ) """
        recv_where = """ AND shf_goods.STATUS = 3 """
        cancel_where = """ AND shf_goods.STATUS = - 1 """

        all_order = cursor.query(command.format(flag=1, fetch_where=fetch_where))
        wait_order = cursor.query(command.format(flag=0, fetch_where=fetch_where + wait_where))
        recv_order = cursor.query(command.format(flag=0, fetch_where=fetch_where + recv_where))
        cancel_order = cursor.query(command.format(flag=0, fetch_where=fetch_where + cancel_where))

        data = {
            'all_order': all_order,
            'wait_order': wait_order,
            'recv_order': recv_order,
            'cancel_order': cancel_order
        }

        return data
