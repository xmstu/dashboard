# -*- coding: utf-8 -*-
from server import log
from server.meta.decorators import make_decorator


class GoodsList(object):

    @staticmethod
    def get_goods_list(cursor, page, limit, params):
        fileds = """
                shf_goods.id,
                shf_goods.NAME,
                shf_goods.weight,
                shf_goods.volume,
                shf_goods.type,
                shf_goods.goods_level,
                shf_goods.haul_dist,-- 旧车型
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
                FROM_UNIXTIME( shf_goods.create_time, '%Y-%m-%d %H:%I:%S' ) AS shf_goods_create_time
        """

        command = """
                    SELECT 
                    %s
                    FROM shf_goods
                    LEFT JOIN shu_users ON shf_goods.user_id = shu_users.id
                    WHERE 1=1
                    -- 货源id
                    -- AND shf_goods.id = 1
                    -- 货主手机
                    -- AND shu_users.mobile = 1
                    -- 出发地
                    -- AND (shf_goods.from_province_id = 1 OR shf_goods.from_city_id = 1 OR shf_goods.from_county_id = 1 OR shf_goods.from_town_id = 1)
                    -- 目的地
                    -- AND (shf_goods.to_province_id = 1 OR shf_goods.to_city_id = 1 OR shf_goods.to_county_id = 1 OR shf_goods.to_town_id = 1)
                    -- 货源类型
                    -- AND shf_goods.haul_dist = 1 AND shf_goods.type = 1
                    -- AND shf_goods.haul_dist = 2 AND shf_goods.goods_level = 2 AND shf_goods.type = 1
                    -- AND shf_goods.haul_dist = 2 AND shf_goods.goods_level = 1 AND shf_goods.type = 1
                    -- AND shf_goods.type = 2
                    -- 货源状态
                    AND shf_goods.status = 1
                    -- AND shf_goods.status = 3
                    -- AND shf_goods.status = -1
                    -- AND shf_goods.expired_timestamp < UNIX_TIMESTAMP()
                    -- 是否通话
                    -- AND (SELECT COUNT(*)
                    -- FROM shu_call_records
                    -- WHERE source_type = 1
                    -- AND source_id = shf_goods.id
                    -- AND (owner_id = shf_goods.user_id OR user_id = shf_goods.user_id)) > 0
                    -- AND (SELECT COUNT(*)
                    -- FROM shu_call_records
                    -- WHERE source_type = 1
                    -- AND source_id = shf_goods.id
                    -- AND (owner_id = shf_goods.user_id OR user_id = shf_goods.user_id)) = 0
                    -- AND (SELECT COUNT(*)
                    -- FROM shu_call_records
                    -- WHERE source_type = 1
                    -- AND source_id = shf_goods.id
                    -- AND (owner_id = shf_goods.user_id OR user_id = shf_goods.user_id)) > 10
        """

        if params['mobile']:
            pass

        goods_count = cursor.query_one(command % "COUNT(*) as goods_count")['goods_count']

        command += """LIMIT %s, %s""" % ((page - 1) * limit, limit)

        log.info('sql:{}'.format(command % fileds))
        goods_detail = cursor.query(command % fileds)

        log.info('goods_detail:{}'.format(goods_detail))

        goods_list = {'goods_detail': goods_detail if goods_detail else [],
                      'goods_count': goods_count if goods_count else 0}

        return goods_list
