# -*- coding: utf-8 -*-
from server import log


class UserList(object):
    @staticmethod
    def get_user_home_station_by_int(cursor, region_id):
        """常驻地查询"""
        command = '''
        SELECT user_id
        FROM tb_inf_user
        WHERE is_deleted = 0
        AND (
        from_province_id = :region_id
        OR from_city_id = :region_id
        OR from_county_id = :region_id
        OR from_town_id = :region_id)'''

        result = cursor.query(command, {
            'region_id': region_id
        })

        return [str(i['user_id']) for i in result if i] if result else []

    @staticmethod
    def get_user_home_station_by_list(cursor, region_id):
        """常驻地查询"""
        command = '''
        SELECT user_id
        FROM tb_inf_user
        WHERE is_deleted = 0
        AND (%s)'''

        region = '''
        from_province_id IN (%(region_id)s)
        OR from_city_id IN (%(region_id)s)
        OR from_county_id IN (%(region_id)s)
        OR from_town_id IN (%(region_id)s)''' % {'region_id': ','.join(region_id)}

        command = command % region

        result = cursor.query(command)

        return [str(i['user_id']) for i in result if i] if result else []

    @staticmethod
    def get_user_list(cursor, page, limit, params):
        try:
            fetch_where = ''''''

            # 查询字段
            fields = '''
            user_id,
            user_name,
            mobile,
            user_type,
            goods_auth,
            driver_auth,
            company_auth,
            goods_count_SH,
            goods_count_LH,
            order_count_SH,
            order_count_LH,
            order_finished_count_SH_online,
            order_finished_count_SH_unline,
            order_finished_count_LH_online,
            order_finished_count_LH_unline,
            download_channel,
            from_channel,
            FROM_UNIXTIME(last_login_time, '%Y-%m-%d') AS last_login_time,
            FROM_UNIXTIME(create_time, '%Y-%m-%d') AS create_time,
            from_province_id,
            from_city_id,
            from_county_id
            '''

            command = """
                SELECT
                {fields}
                FROM tb_inf_user
    
                WHERE is_deleted = 0
                {fetch_where}
                """

            # 地区
            region = ''
            if params['region_id']:
                if isinstance(params['region_id'], int):
                    region = 'AND (from_province_id = %(region_id)s OR from_city_id = %(region_id)s OR from_county_id = %(region_id)s OR from_town_id = %(region_id)s) ' % {
                        'region_id': params['region_id']}
                elif isinstance(params['region_id'], list):
                    region = '''AND (
                                from_province_id IN (%(region_id)s)
                                OR from_city_id IN (%(region_id)s)
                                OR from_county_id IN (%(region_id)s)
                                OR from_town_id IN (%(region_id)s)
                                ) ''' % {'region_id': ','.join(params['region_id'])}
            fetch_where += region

            # 用户名
            if params['user_name']:
                fetch_where += 'AND user_name = "%s" ' % params['user_name']
            # 手机号
            if params['mobile']:
                fetch_where += 'AND mobile = "%s" ' % params['mobile']
            # 推荐人手机
            if params['reference_mobile']:
                fetch_where += 'AND referrer_mobile = "%s" ' % params['reference_mobile']
            # 下载渠道
            if params['download_ch']:
                fetch_where += 'AND download_channel = "%s" ' % params['download_ch']
            # 注册渠道
            if params['from_channel']:
                fetch_where += 'AND from_channel = "%s" ' % params['from_channel']
            # 推荐注册
            if params['is_referenced'] == 1:
                fetch_where += 'AND referrer_mobile != "" '
            elif params['is_referenced'] == 2:
                fetch_where += 'AND referrer_mobile = "" '
            # 注册角色
            if params['role_type'] == 1:
                fetch_where += 'AND user_type = 1 '
            elif params['role_type'] == 2:
                fetch_where += 'AND user_type = 2 '
            elif params['role_type'] == 3:
                fetch_where += 'AND user_type = 3 '
            # 认证角色
            if params['role_auth'] == 1:
                fetch_where += 'AND goods_auth = 1 '
            elif params['role_auth'] == 2:
                fetch_where += 'AND driver_auth = 1 '
            elif params['role_auth'] == 3:
                fetch_where += 'AND company_auth = 1 '
            # 是否活跃
            if params['is_actived'] == 1:
                fetch_where += 'AND keep_login_days >= 7 AND last_login_time > UNIX_TIMESTAMP() - 1 * 86400 '
            elif params['is_actived'] == 2:
                fetch_where += '''AND last_login_time < UNIX_TIMESTAMP() - 1 * 86400
                AND last_login_time > UNIX_TIMESTAMP() - 3 * 86400 '''
            elif params['is_actived'] == 3:
                fetch_where += '''AND last_login_time < UNIX_TIMESTAMP() - 4 * 86400
                AND last_login_time > UNIX_TIMESTAMP() - 10 * 86400 '''
            elif params['is_actived'] == 4:
                fetch_where += '''AND last_login_time < UNIX_TIMESTAMP() - 10 * 86400 '''

            # 操作过
            if params['is_used'] == 1:
                fetch_where += 'AND (goods_count_LH > 0 OR goods_count_SH > 0) '
            elif params['is_used'] == 2:
                fetch_where += 'AND (order_count_SH > 0 OR order_count_SH > 0) '
            elif params['is_used'] == 3:
                fetch_where += 'AND ( order_finished_count_SH_online > 0 OR order_finished_count_SH_unline > 0 OR order_finished_count_LH_online > 0 OR order_finished_count_LH_unline > 0 ) '

            # 贴车贴
            if params['is_car_sticker'] == 1:
                fetch_where += 'AND is_sticker > 0 '
            elif params['is_car_sticker'] == 2:
                fetch_where += 'AND is_sticker = 0 '
            # 最后登录
            if params['last_login_start_time'] and params['last_login_end_time']:
                fetch_where += 'AND last_login_time >= %s AND last_login_time < %s ' % (
                    params['last_login_start_time'], params['last_login_end_time'])
            # 注册日期
            if params['register_start_time'] and params['register_end_time']:
                fetch_where += 'AND create_time >= %s AND create_time < %s ' % (
                    params['register_start_time'], params['register_end_time'])

            user_count = cursor.query_one(command.format(fields="COUNT(1) AS count", fetch_where=fetch_where))

            fetch_where += """ ORDER BY id DESC LIMIT %s, %s """ % ((page - 1) * limit, limit)
            # 详情
            user_detail = cursor.query(command.format(fields=fields, fetch_where=fetch_where))

            user_list = {
                'user_detail': user_detail if user_detail else [],
                'user_count': user_count['count'] if user_count['count'] else 0
            }

            return user_list
        except Exception as e:
            log.error(e)


class UserStatistic(object):

    @staticmethod
    def get_before_user_count_by_mobile(cursor, params, user_ids):
        """累计用户"""
        command = """
        SELECT COUNT(1) AS count
        FROM shu_users
        INNER JOIN shu_user_profiles ON shu_users.id = shu_user_profiles.user_id
        LEFT JOIN shu_user_auths AS goods_auth ON goods_auth.id = shu_user_profiles.last_auth_goods_id AND goods_auth.auth_status = 2 AND goods_auth.is_deleted = 0
        LEFT JOIN shu_user_auths AS driver_auth ON driver_auth.id = shu_user_profiles.last_auth_driver_id AND driver_auth.auth_status = 2 AND driver_auth.is_deleted = 0
        LEFT JOIN shu_user_auths AS company_auth ON company_auth.id = shu_user_profiles.last_auth_company_id AND company_auth.auth_status = 2 AND company_auth.is_deleted = 0

        WHERE shu_users.is_deleted = 0
        AND shu_users.create_time < :start_time
        -- 角色
        AND ((:role_type = 0)
        OR (:role_type = 1 AND shu_user_profiles.user_type = 1)
        OR (:role_type = 2 AND shu_user_profiles.user_type = 2)
        OR (:role_type = 3 AND shu_user_profiles.user_type = 3)
        )
        -- 认证
        AND ((:is_auth = 0)
        OR (:is_auth = 1 AND (goods_auth.auth_goods = 1 OR driver_auth.auth_driver = 1 OR company_auth.auth_company = 1))
        OR (:is_auth = 2 AND (goods_auth.auth_goods IS NULL AND driver_auth.auth_driver IS NULL AND company_auth.auth_company IS NULL))
        )
        %s
        """

        # 地区限制
        region = ''
        if user_ids:
            region = 'AND shu_users.id IN (%s)' % ','.join(user_ids)

        # 优化查询速度
        if not params['role_type'] and not params['is_auth']:
            cmd = """
            SELECT COUNT(1) AS count
            FROM shu_users
            WHERE shu_users.is_deleted = 0 AND shu_users.create_time < :start_time
            %s
            """
            cmd = cmd % region
            before_user_count = cursor.query_one(cmd, {'start_time': params['start_time']})
        else:
            # 地区限制
            region = ''
            if user_ids:
                region = 'AND shu_users.id IN (%s)' % ','.join(user_ids)

            # region = ''
            # if params['region_id']:
            #     region = 'AND SUBSTRING_INDEX(shu_user_profiles.mobile_area, " ", -1) IN (%s)' % ','.join(
            #         params['region_id'])

            command = command % region

            before_user_count = cursor.query_one(command, {
                'start_time': params['start_time'],
                'role_type': params['role_type'],
                'is_auth': params['is_auth']
            })

        return before_user_count['count'] if before_user_count else 0

    @staticmethod
    def get_user_statistic_by_mobile(cursor, params, user_ids=None):
        """用户变化趋势"""
        command = """
        SELECT
        FROM_UNIXTIME(shu_users.create_time, '%%%%Y-%%%%m-%%%%d') AS create_time,
        COUNT(1) AS count

        FROM shu_users
        INNER JOIN shu_user_profiles ON shu_users.id = shu_user_profiles.user_id
        LEFT JOIN shu_user_auths AS goods_auth ON goods_auth.id = shu_user_profiles.last_auth_goods_id AND goods_auth.auth_status = 2 AND goods_auth.is_deleted = 0
        LEFT JOIN shu_user_auths AS driver_auth ON driver_auth.id = shu_user_profiles.last_auth_driver_id AND driver_auth.auth_status = 2 AND driver_auth.is_deleted = 0
        LEFT JOIN shu_user_auths AS company_auth ON company_auth.id = shu_user_profiles.last_auth_company_id AND company_auth.auth_status = 2 AND company_auth.is_deleted = 0

        WHERE shu_users.is_deleted = 0
        AND shu_users.create_time >= :start_time
        AND shu_users.create_time < :end_time
        -- 角色
        AND ((:role_type = 0)
        OR (:role_type = 1 AND shu_user_profiles.user_type = 1)
        OR (:role_type = 2 AND shu_user_profiles.user_type = 2)
        OR (:role_type = 3 AND shu_user_profiles.user_type = 3)
        )
        -- 认证
        AND ((:is_auth = 0)
        OR (:is_auth = 1 AND (goods_auth.auth_goods = 1 OR driver_auth.auth_driver = 1 OR company_auth.auth_company = 1))
        OR (:is_auth = 2 AND (goods_auth.auth_goods IS NULL AND driver_auth.auth_driver IS NULL AND company_auth.auth_company IS NULL))
        )
        %s
        GROUP BY FROM_UNIXTIME(shu_users.create_time, '%%%%Y-%%%%m-%%%%d')
        """
        region = ''
        if user_ids:
            region = 'AND shu_users.id IN (%s)' % ','.join(user_ids)

        command = command % region

        user_statistic = cursor.query(command, {
            'start_time': params['start_time'],
            'end_time': params['end_time'],
            'role_type': params['role_type'],
            'is_auth': params['is_auth']
        })

        return user_statistic if user_statistic else []
