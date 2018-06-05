
class CityOrderListModel(object):

    @staticmethod
    def get_data(cursor, page, limit, params):

        fields = """
                shf_goods.id,
                shf_goods.NAME,
                shf_goods.weight,
                shf_goods.volume,
                shf_goods.type,
                shf_goods.goods_level,
                shf_goods.haul_dist,
                # TODO 优化
                ( SELECT shm_regions.full_short_name FROM shm_regions WHERE shf_goods.from_city_id = shm_regions.`code` ) AS from_full_name,
                ( SELECT shm_regions.short_name FROM shm_regions WHERE shf_goods.from_city_id = shm_regions.`code` ) AS from_short_name,
                ( SELECT shm_regions.full_short_name FROM shm_regions WHERE shf_goods.to_city_id = shm_regions.`code` ) AS to_full_name,
                ( SELECT shm_regions.short_name FROM shm_regions WHERE shf_goods.to_city_id = shm_regions.`code` ) AS to_short_name,
                shf_goods.from_address,
                shf_goods.to_address,
                shf_goods.mileage_total,
                shf_goods.STATUS,
                (
                SELECT
                IF
                    ( shf_goods_vehicles.attribute_value_id = 0, '不限车型', GROUP_CONCAT( shm_dictionary_items.NAME ) ) 
                FROM
                    shf_goods_vehicles
                    LEFT JOIN shm_dictionary_items ON shf_goods_vehicles.attribute_value_id = shm_dictionary_items.id 
                    AND shm_dictionary_items.is_deleted = 0 
                WHERE
                    shf_goods_vehicles.goods_id = shf_goods.id 
                    AND shf_goods_vehicles.vehicle_attribute = 1 
                    AND shf_goods_vehicles.is_deleted = 0 
                ) AS vehicle_type,
                (
                SELECT
                IF
                    ( shf_goods_vehicles.attribute_value_id = 0, '不限车长', GROUP_CONCAT( shm_dictionary_items.NAME ) ) 
                FROM
                    shf_goods_vehicles
                    LEFT JOIN shm_dictionary_items ON shf_goods_vehicles.attribute_value_id = shm_dictionary_items.id 
                    AND shm_dictionary_items.is_deleted = 0 
                WHERE
                    shf_goods_vehicles.goods_id = shf_goods.id 
                    AND shf_goods_vehicles.vehicle_attribute = 2 
                    AND shf_goods_vehicles.is_deleted = 0 
                ) AS vehicle_length,-- 新车型
                (
                SELECT
                    shf_goods_vehicles.NAME 
                FROM
                    shf_goods_vehicles 
                WHERE
                    shf_goods_vehicles.goods_id = shf_goods.id 
                    AND shf_goods_vehicles.vehicle_attribute = 3 
                    AND shf_goods_vehicles.is_deleted = 0 
                ) AS new_vehicle_type,
                (
                SELECT
                    shm_dictionary_items.NAME 
                FROM
                    shf_goods_vehicles
                    LEFT JOIN shm_dictionary_items ON shf_goods_vehicles.attribute_value_id = shm_dictionary_items.id 
                    AND shm_dictionary_items.is_deleted = 0 
                WHERE
                    shf_goods_vehicles.goods_id = shf_goods.id 
                    AND shf_goods_vehicles.vehicle_attribute = 3 
                    AND shf_goods_vehicles.is_deleted = 0 
                ) AS new_vehicle_length,
                shf_goods.price_recommend,
                shf_goods.price_expect,
                shf_goods.price_addition,
                shu_users.mobile,
                ( SELECT COUNT( * ) FROM shf_goods WHERE user_id = shu_users.id ) AS shf_goods_counts,
                (
                SELECT
                    COUNT( * ) 
                FROM
                    shu_call_records 
                WHERE
                    source_type = 1 
                    AND source_id = shf_goods.id 
                    AND ( owner_id = shf_goods.user_id OR user_id = shf_goods.user_id ) 
                ) AS call_count,
                FROM_UNIXTIME( shf_goods.create_time, '%Y-%m-%d %H:%I:%S' ) AS shf_goods_create_time,-- 旧版装货时间
                shf_goods.loading_time_date,
                shf_goods.loading_time_period,-- 新版装货时间
                shf_goods.loading_time_period_begin 
        """

        command = """
            SELECT
                %s 
            FROM
                shf_goods
                LEFT JOIN shu_users ON shf_goods.user_id = shu_users.id 
            WHERE
                1 = 1 
            -- 同城普通货源
            -- AND shf_goods.haul_dist = 1 
            -- AND shf_goods.type = 1 
            -- 跨城定价普通货源
            -- AND shf_goods.haul_dist = 2 AND shf_goods.goods_level = 2 AND shf_goods.type = 1
            -- 跨城议价普通货源
            -- AND shf_goods.haul_dist = 2 AND shf_goods.goods_level = 1 AND shf_goods.type = 1
            -- 零担货源
            -- AND shf_goods.type = 2
            
            -- 优先级
            -- 车长
            
            
            -- 是否通话
            -- 	AND (
            -- 	SELECT
            -- 		COUNT( * ) 
            -- 	FROM
            -- 		shu_call_records 
            -- 	WHERE
            -- 		source_type = 1 
            -- 		AND source_id = shf_goods.id 
            -- 		AND ( owner_id = shf_goods.user_id OR user_id = shf_goods.user_id ) 
            -- 	) > 0 
            
            -- 是否加价
            -- 	AND shf_goods.price_addition > 0 -- 所属网点
            
            -- 是否初次下单
            -- 	AND ( SELECT COUNT( * ) FROM shf_goods WHERE user_id = shu_users.id ) = 1
        """

        # 货源类型
        if params.get('goods_type'):
            if params['goods_type'] == 1:
                command += """ AND shf_goods.haul_dist = 1 AND shf_goods.type = 1 """
            if params['goods_type'] == 2:
                command += """ AND shf_goods.haul_dist = 2 AND shf_goods.goods_level = 2 AND shf_goods.type = 1 """
            if params['goods_type'] == 3:
                command += """ AND shf_goods.haul_dist = 2 AND shf_goods.goods_level = 1 AND shf_goods.type = 1 """

        # 优先级
        if params.get('priority'):
            pass

        # 车长
        if params.get('vehicle_length'):
            pass

        # 是否通话
        if params.get('is_called'):
            called_sql = """ AND (SELECT COUNT(*)
                            FROM shu_call_records
                            WHERE source_type = 1
                            AND source_id = shf_goods.id
                            AND (owner_id = shf_goods.user_id OR user_id = shf_goods.user_id)) """
            if params['is_called'] == 1:
                command += called_sql + '> 0 '
            if params['is_called'] == 2:
                command += called_sql + '= 0 '
            if params['is_called'] == 3:
                command += called_sql + '> 10 '

        # 是否加价
        if params.get('is_addition'):
            if params['is_addition'] == 1:
                command += ' AND shf_goods.price_addition > 0 '
            elif params['is_addition'] == 2:
                command += ' AND shf_goods.price_addition = 0 '

        # 所属网点
        if params.get('node_id'):
            pass

        # 是否初次下单
        if params.get('new_goods_type') > 0:
            command += """ AND ( SELECT COUNT( * ) FROM shf_goods WHERE user_id = shu_users.id ) = 1 """

        order_counts = cursor.query_one(command % "COUNT(*) as order_counts")['order_counts']

        command += """ LIMIT {0}, {1} """.format((page - 1) * limit, limit)

        order_detail = cursor.query(command % fields)

        data = {
            'order_detail': order_detail if order_detail else [],
            'order_counts': order_counts if order_counts else 0,
        }

        return data
