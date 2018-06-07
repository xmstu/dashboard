# -*- coding: utf-8 -*-


class PromoteEffetList(object):
    @staticmethod
    def get_promote_effet_list(cursor, page, limit, params):

        # 查询字段
        fileds = """
            -- 名字
            shu_user_profiles.user_name,
            -- 手机号
            shu_users.mobile,
            -- 推荐人数
            -- 唤醒人数
            -- 发货数
            -- 发货人数
            -- 完成数
            -- 货源金额
            -- 完成金额
        """

        command = """
                SELECT
                    %s
                FROM
                    shu_users
                    LEFT JOIN shu_user_profiles ON shu_users.id = shu_user_profiles.user_id
                    LEFT JOIN shu_user_stats ON shu_users.id = shu_user_stats.user_id 
                WHERE
                    shu_users.is_deleted = 0
                -- 	ANd shu_user_profiles.user_name = '猫大'
                -- 	AND shu_users.mobile = 15917907641
                    -- 所属地区
                    -- 推荐角色
                    -- 货源类型
                    -- 是否活跃
                    -- 贴车贴
                    -- AND shu_user_profiles.trust_member_type = 2 AND ad_expired_time > UNIX_TIMESTAMP()
                    -- AND shu_user_profiles.trust_member_type != 2
                    -- 注册日期
        """

        # TODO 语句需要优化

        promote_counts = cursor.query_one(command % "COUNT(*) AS promote_counts")['promote_counts']

        # 分页
        command += """ LIMIT %s, %s """ % ((page - 1) * limit, limit)

        promote_effet_detail = cursor.query(command)

        promote_effet_list = {
            'promote_effet_detail': promote_effet_detail if promote_effet_detail else [],
            'count': promote_counts if promote_counts else 0,
        }

        return promote_effet_list if promote_effet_list else None


class PromoteQuality(object):

    @staticmethod
    def get_promote_quality(cursor, params):

        # 拉新 - 新增 累计
        if params.get('dimension') == 1:
            promote_quality = get_new_users(cursor, params)

        # 用户行为 - 登录 发货 接单 完成订单
        if params.get('dimension') == 2:
            promote_quality = get_user_behavior(cursor, params)

        # 金额 - 货源总额 订单总额 实际完成总额
        if params.get('dimension') == 3:
            promote_quality = get_money(cursor, params)


        return promote_quality if promote_quality else []


def get_new_users(cursor, params):

    command = """ 
            SELECT create_time, COUNT(*)
            FROM tb_inf_user
            -- 时间段
            WHERE UNIX_TIMESTAMP(create_time) >= :start_time
            AND UNIX_TIMESTAMP(create_time) < :end_time
            -- 推荐人
            AND reference_id IS NOT NULL
            -- 地区
            AND (from_province_id = :region_id OR from_city_id = :region_id OR from_county_id = :region_id OR from_town_id = :region_id)

            GROUP BY create_time;
             """

    promote_quality = cursor.query(command, {
        'start_time': params['start_time'],
        'end_time': params['end_time'],
        'region_id': params['region_id'],
    })

    return promote_quality


def get_user_behavior(cursor, params):
    if params.get('type') == 1:
        command = """
            -- 用户登录
            SELECT create_time, COUNT(*)
            FROM tb_inf_user
            -- 时间段
            WHERE UNIX_TIMESTAMP(create_time) >= :start_time
            AND UNIX_TIMESTAMP(create_time) < :end_time
            -- 推荐人
            AND reference_id IS NOT NULL
            -- 地区
            AND (from_province_id = :region_id OR from_city_id = :region_id OR from_county_id = :region_id OR from_town_id = :region_id)
            -- 登录
            AND last_login_time >= :start_time
            AND last_login_time < :end_time
            GROUP BY create_time;
        """

    if params.get('type') == 2:
        command = """ 
             -- 用户发货
            SELECT tb_inf_user.create_time, COUNT(*)
            FROM tb_inf_user
            INNER JOIN tb_inf_goods ON tb_inf_user.user_id = tb_inf_goods.user_id
            AND UNIX_TIMESTAMP(tb_inf_goods.create_time) >= :start_time
            AND UNIX_TIMESTAMP(tb_inf_goods.create_time) < :end_time
            -- 时间段
            WHERE UNIX_TIMESTAMP(tb_inf_user.create_time) >= :start_time
            AND UNIX_TIMESTAMP(tb_inf_user.create_time) < :end_time
            -- 推荐人
            AND reference_id IS NOT NULL
            -- 地区
            AND (from_province_id = :region_id OR from_city_id = :region_id OR from_county_id = :region_id OR from_town_id = :region_id)

            GROUP BY create_time;
         """

    if params.get('type') == 3:
        command = """
            -- 用户接单
            SELECT tb_inf_user.create_time, COUNT(*)
            FROM tb_inf_user
            INNER JOIN tb_inf_order ON tb_inf_user.user_id = tb_inf_order.user_id
            AND UNIX_TIMESTAMP(tb_inf_order.create_time) >= :start_time
            AND UNIX_TIMESTAMP(tb_inf_order.create_time) < :end_time
            -- 时间段
            WHERE UNIX_TIMESTAMP(tb_inf_user.create_time) >= :start_time
            AND UNIX_TIMESTAMP(tb_inf_user.create_time) < :end_time
            -- 推荐人
            AND reference_id IS NOT NULL
            -- 地区
            AND (from_province_id = :region_id OR from_city_id = :region_id OR from_county_id = :region_id OR from_town_id = :region_id)
            
            GROUP BY create_time;
         """

    if params.get('type') == 4:
        command = """
            -- 用户完成订单
            SELECT tb_inf_user.create_time, COUNT(*)
            FROM tb_inf_user
            INNER JOIN tb_inf_order ON tb_inf_user.user_id = tb_inf_order.user_id
            AND UNIX_TIMESTAMP(tb_inf_order.create_time) >= :start_time
            AND UNIX_TIMESTAMP(tb_inf_order.create_time) < :end_time
            AND tb_inf_order.`status` = 3
            -- 时间段
            WHERE UNIX_TIMESTAMP(tb_inf_user.create_time) >= :start_time
            AND UNIX_TIMESTAMP(tb_inf_user.create_time) < :end_time
            -- 推荐人
            AND reference_id IS NOT NULL
            -- 地区
            AND (from_province_id = :region_id OR from_city_id = :region_id OR from_county_id = :region_id OR from_town_id = :region_id)

            GROUP BY create_time;
        """

    promote_quality = cursor.query(command, {
        'start_time': params['start_time'],
        'end_time': params['end_time'],
        'region_id': params['region_id'],
    })

    return promote_quality


def get_money(cursor, params):
    if params.get('type') == 1:
        command = """
            -- 用户货源总额
            SELECT tb_inf_user.create_time, SUM(goods_price_sum)
            FROM tb_inf_user
            INNER JOIN tb_inf_goods ON tb_inf_user.user_id = tb_inf_goods.user_id
            AND UNIX_TIMESTAMP(tb_inf_goods.create_time) >= :start_time
            AND UNIX_TIMESTAMP(tb_inf_goods.create_time) < :end_time
            
            -- 时间段
            WHERE UNIX_TIMESTAMP(tb_inf_user.create_time) >= :start_time
            AND UNIX_TIMESTAMP(tb_inf_user.create_time) < :end_time
            -- 推荐人
            AND reference_id IS NOT NULL
            -- 地区
            AND (from_province_id = :region_id OR from_city_id = :region_id OR from_county_id = :region_id OR from_town_id = :region_id)
            GROUP BY create_time;
        """
    if params.get('type') == 2:
        command = """
            -- 用户订单总额
            SELECT tb_inf_user.create_time, SUM(order_price_sum)
            FROM tb_inf_user
            INNER JOIN tb_inf_order ON tb_inf_user.user_id = tb_inf_order.user_id
            AND UNIX_TIMESTAMP(tb_inf_order.create_time) >= :start_time
            AND UNIX_TIMESTAMP(tb_inf_order.create_time) < :end_time
            
            -- 时间段
            WHERE UNIX_TIMESTAMP(tb_inf_user.create_time) >= :start_time
            AND UNIX_TIMESTAMP(tb_inf_user.create_time) < :end_time
            -- 推荐人
            AND reference_id IS NOT NULL
            -- 地区
            AND (from_province_id = :region_id OR from_city_id = :region_id OR from_county_id = :region_id OR from_town_id = :region_id)
            -- 登录
            -- AND last_login_time >= UNIX_TIMESTAMP('2018-04-01')
            -- AND last_login_time < UNIX_TIMESTAMP('2018-05-01')
            --
            GROUP BY create_time;
        """
    if params.get('type') == 3:
        command = """
                -- 用户订单完成总额
                SELECT tb_inf_user.create_time, SUM(order_price_sum)
                FROM tb_inf_user
                INNER JOIN tb_inf_order ON tb_inf_user.user_id = tb_inf_order.user_id
                AND UNIX_TIMESTAMP(tb_inf_order.create_time) >= :start_time
                AND UNIX_TIMESTAMP(tb_inf_order.create_time) < :end_time
                AND tb_inf_order.`status` = 3
                
                -- 时间段
                WHERE UNIX_TIMESTAMP(tb_inf_user.create_time) >= :start_time
                AND UNIX_TIMESTAMP(tb_inf_user.create_time) < :end_time
                -- 推荐人
                AND reference_id IS NOT NULL
                -- 地区
                AND (from_province_id = :region_id OR from_city_id = :region_id OR from_county_id = :region_id OR from_town_id = :region_id)
                GROUP BY create_time;
                """

    promote_quality = cursor.query(command, {
        'start_time': params['start_time'],
        'end_time': params['end_time'],
        'region_id': params['region_id'],
    })

    return promote_quality
