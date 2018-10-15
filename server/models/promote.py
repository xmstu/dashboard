# -*- coding: utf-8 -*-
import time

from flask_restful import abort

from server import log
from server.status import HTTPStatus, make_resp, APIStatus


class PromoteEffectList(object):
    @staticmethod
    def get_promoter_mobile_by_city_manage(cursor, params):
        """城市经理获取推广人员信息"""
        command = """
        SELECT
            tb_inf_promoter.mobile 
        FROM
            tb_inf_promoter 
        WHERE
            tb_inf_promoter.is_deleted = 0 
            AND role_id = :role_id
            %s
        """
        fetch_where = ''
        # 用户名
        if params.get('user_name'):
            fetch_where += "AND tb_inf_promoter.user_name = '%s' " % params['user_name']
        # 手机号
        if params.get('mobile'):
            fetch_where += "AND tb_inf_promoter.mobile = '%s' " % params['mobile']

        command = command % fetch_where
        result = cursor.query(command, params)

        return [i['mobile'] for i in result if i['mobile']] if result else []

    @staticmethod
    def get_promoter_mobile_by_admin(cursor, params):
        """其他人获取推广人员"""
        command = """
        SELECT mobile
        FROM tb_inf_user
        WHERE is_deleted = 0
        AND mobile IN (
        SELECT DISTINCT referrer_mobile
        FROM tb_inf_user
        WHERE referrer_mobile != '')
        %s
        """
        fetch_where = ''
        # 用户名
        if params['user_name']:
            fetch_where += "AND user_name = '%s' " % params['user_name']
        # 手机号
        if params['mobile']:
            fetch_where += "AND mobile = '%s' " % params['mobile']

        command = command % fetch_where
        result = cursor.query(command)

        return [i['mobile'] for i in result if i['mobile']] if result else []

    @staticmethod
    def get_promote_list(read_bi, read_db, params, referrer_mobile):
        """获取推广人员列表"""

        command = """
        SELECT
            referrer.*,
        -- 	注册货主数
            (SELECT COUNT(DISTINCT user_id) FROM tb_inf_user 
            WHERE referrer_mobile = referrer.mobile AND recommended_status = 2
            AND user_type = 1 AND {bi_fetch_where}) AS register_owner_count,
        -- 注册司机数
            (SELECT COUNT(DISTINCT user_id) FROM tb_inf_user 
            WHERE referrer_mobile = referrer.mobile AND recommended_status = 2 AND user_type = 2 
            AND {bi_fetch_where}) AS register_driver_count,
        -- 认证司机数
            (SELECT COUNT(DISTINCT user_id) FROM tb_inf_user 
            WHERE referrer_mobile = referrer.mobile AND recommended_status = 2
            AND driver_auth = 1 AND {bi_fetch_where}) AS auth_driver_count
        FROM
            (
            SELECT
                user_id,
            IF
                ( tb_inf_promoter.user_name != '', tb_inf_promoter.user_name, tb_inf_user.user_name ) AS user_name,
                tb_inf_promoter.mobile 
            FROM
                tb_inf_promoter
                LEFT JOIN tb_inf_user ON tb_inf_user.mobile = tb_inf_promoter.mobile 
                AND tb_inf_user.is_deleted = 0 
            WHERE
                tb_inf_promoter.is_deleted = 0 
                AND tb_inf_promoter.mobile IN (%s) 
            ) AS referrer
        GROUP BY
            referrer.mobile;
        """

        promote_mobile = ','.join(referrer_mobile)
        bi_fetch_where = ' 1=1 '
        db_goods_fetch_where = ' 1=1 '
        db_orders_fetch_where = ' 1=1 '

        # 注册日期
        if params['register_start_time'] and params['register_end_time']:
            bi_fetch_where += """ 
            AND create_time >= {} AND create_time < {} 
            """.format(params['register_start_time'], params['register_end_time'])

        # 统计时间
        if params['statistic_start_time'] and params['statistic_end_time']:
            db_goods_fetch_where += """
            AND create_time >= {0} AND create_time < {1}
            """.format(params['statistic_start_time'], params['statistic_end_time'])
            db_orders_fetch_where += """
            AND so.create_time >= {0} AND so.create_time < {1}
            """.format(params['statistic_start_time'], params['statistic_end_time'])

        # 一口价/议价
        if params['goods_type']:
            db_goods_fetch_where += """
            AND (
            ({goods_type}=1 AND is_system_price = 1) OR
            ({goods_type}=2 AND is_system_price = 0)
            )
            """.format(goods_type=params['goods_type'])
            db_orders_fetch_where += """
            AND (
            ({goods_type}=1 AND sg.is_system_price = 1) OR
            ({goods_type}=2 AND sg.is_system_price = 0)
            )
            """.format(goods_type=params['goods_type'])

        command = command % promote_mobile
        try:
            bi_ret = read_bi.query(command.format(bi_fetch_where=bi_fetch_where))
            db_ret = PromoteEffectList.get_data_from_db(read_bi, read_db, referrer_mobile, bi_fetch_where, db_goods_fetch_where, db_orders_fetch_where)
            for i in bi_ret:
                for j in db_ret:
                    if i['mobile'] == j['mobile']:
                        i.update(j)
                        break

            return bi_ret if bi_ret else []
        except Exception as e:
            log.error('推广统计列表无法获取数据,错误原因是:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='内部服务器错误'))

    @staticmethod
    def get_data_from_db(read_bi, read_db, referrer_mobile, bi_fetch_where, db_goods_fetch_where, db_orders_fetch_where):
        ret = []
        log.info("推广人手机列表 [referrer_mobile:%r]" % referrer_mobile)
        for promote_mobile in referrer_mobile:
            tb_sql = """
                    SELECT 
                        DISTINCT user_id AS user_id
                    FROM
                        tb_inf_user 
                    WHERE
                        referrer_mobile = {promote_mobile}
                        AND recommended_status = 2 AND {bi_fetch_where}
                    """
            tb_sql = tb_sql.format(promote_mobile=promote_mobile, bi_fetch_where=bi_fetch_where)
            log.info("推广统计查询被推荐人id [tb_sql:%s]" % tb_sql)
            fetch_user = read_bi.query(tb_sql)
            try:
                fetch_user_id_str = ','.join((str(detail['user_id']) for detail in fetch_user))
                if not fetch_user_id_str:
                    db_data = None
                else:
                    db_sql = """
                            SELECT *
                            FROM
                            (
                            SELECT
                                COUNT( 1 ) AS goods_count,
                                COUNT( DISTINCT sg.user_id ) AS goods_owner_count
                            FROM
                                shf_goods AS sg 
                            WHERE
                                sg.user_id IN (%(fetch_user_id_str)s) 
                                AND {db_goods_fetch_where}
                            ) 
                            AS a,
                            (
                            SELECT
                                COUNT( so.owner_id ) AS goods_received_count
                            FROM
                                shb_orders AS so
                                INNER JOIN shf_goods AS sg ON sg.id = so.goods_id 
                            WHERE
                                so.`status` != -1
                                AND so.owner_id IN (%(fetch_user_id_str)s) 
                                AND {db_orders_fetch_where}
                            ) 
                            AS b,
                            (
                            SELECT
                                COUNT( so.driver_id  ) AS accept_order_count
                            FROM
                                shb_orders AS so
                                INNER JOIN shf_goods AS sg ON sg.id = so.goods_id 
                            WHERE
                                so.driver_id IN (%(fetch_user_id_str)s) 
                                AND {db_orders_fetch_where}
                            ) 
                            AS c,
                            (
                            SELECT
                                COUNT( su.id ) AS sticker_driver_count
                            FROM
                                sml_ads AS sml_ads
                                INNER JOIN shu_users AS su ON su.mobile = sml_ads.driver_mobile 
                                AND sml_ads.audit = 2 
                            WHERE
                                su.id IN (%(fetch_user_id_str)s) 
                            ) 
                            AS d
                            """
                    db_sql = db_sql % {'fetch_user_id_str': fetch_user_id_str}
                    db_sql = db_sql.format(db_goods_fetch_where=db_goods_fetch_where,
                                           db_orders_fetch_where=db_orders_fetch_where)
                    log.info("推广统计列表查询sql: [db_sql:%s]" % db_sql)
                    db_data = read_db.query(db_sql)
            except Exception as e:
                log.error("推广统计列表查询失败: [ERROR:%s]" % e)
                db_data = None

            if db_data:
                db_data = db_data[0]
                db_data.setdefault('mobile', promote_mobile)
            else:
                db_data = {
                    'goods_count': 0,
                    'goods_owner_count': 0,
                    'goods_received_count': 0,
                    'accept_order_count': 0,
                    'sticker_driver_count': 0,
                    'mobile': promote_mobile,
                }
            ret.append(db_data)
        return ret

    @staticmethod
    def check_promoter(cursor, params):
        """检查推广人员是否存在"""
        command = '''
        SELECT
            id 
        FROM
            tb_inf_promoter 
        WHERE
            is_deleted = 0
            AND role_id = :role_id 
            AND mobile = :mobile 
        '''
        result = cursor.query_one(command, params)

        return result['id'] if result else None

    @staticmethod
    def add_promoter(cursor, params):
        """添加推广人员"""
        try:
            command = '''
            INSERT INTO tb_inf_promoter(role_id, user_name, mobile)
            VALUES (:role_id, :user_name, :mobile)
            '''
            result = cursor.insert(command, params)

            return result
        except Exception as e:
            log.error('添加推广人员失败: [error: %s]' % e, exc_info=True)

    @staticmethod
    def delete_promoter(cursor, params):
        """删除推广人员"""
        command = '''
        UPDATE tb_inf_promoter
        SET is_deleted = 1
        WHERE mobile = :promoter_mobile
        '''
        result = cursor.update(command, params)

        return result


class PromoteQuality(object):
    @staticmethod
    def get_promoter_mobile_by_city_manager(cursor, params):
        """城市经理获取推广人员信息"""
        command = """
        SELECT
            tb_inf_promoter.mobile 
        FROM
            tb_inf_promoter 
        WHERE
            tb_inf_promoter.is_deleted = 0 
            AND role_id = :role_id
        """
        result = cursor.query(command, params)

        return [i['mobile'] for i in result if i['mobile']] if result else []

    @staticmethod
    def get_promoter_mobile_by_admin(cursor, params):
        """管理员获取推广人员信息"""
        command = """
        SELECT mobile
        FROM tb_inf_promoter
        WHERE is_deleted = 0
        %s
        """
        fetch_where = ''
        # 用户名
        if params.get('user_name'):
            fetch_where += "AND tb_inf_promoter.user_name = '%s' " % params['user_name']
        # 手机号
        if params.get('mobile'):
            fetch_where += "AND tb_inf_promoter.mobile = '%s' " % params['mobile']

        command = command % fetch_where
        result = cursor.query(command)

        return [i['mobile'] for i in result if i['mobile']] if result else []

    @staticmethod
    def get_promoter_mobile_by_suppliers(cursor, city_region, params):
        """区镇合伙人获取推广人员信息"""
        if not city_region:
            return []
        command = """
        SELECT
            mobile
        FROM
            tb_inf_promoter
            INNER JOIN tb_inf_roles ON tb_inf_promoter.role_id = tb_inf_roles.id AND tb_inf_promoter.is_deleted = 0 AND tb_inf_roles.is_deleted = 0
        WHERE
            tb_inf_roles.region_id = %d 
            %s
        """
        fetch_where = ''
        # 用户名
        if params.get('user_name'):
            fetch_where += "AND tb_inf_promoter.user_name = '%s' " % params['user_name']
        # 手机号
        if params.get('mobile'):
            fetch_where += "AND tb_inf_promoter.mobile = '%s' " % params['mobile']

        command = command % (city_region, fetch_where)
        result = cursor.query(command)

        return [i['mobile'] for i in result if i['mobile']] if result else []

    @staticmethod
    def get_promoter_id(cursor, mobile):
        """推广人员id"""
        command = """
        SELECT id
        FROM shu_users
        WHERE is_deleted = 0
        AND mobile IN (%s)
        """
        if mobile:
            command = command % ','.join(["'"+i+"'" for i in mobile])
        else:
            return []
        result = cursor.query(command)

        return [str(i['id']) for i in result] if result else []

    @staticmethod
    def get_new_users(cursor, params, promoter_ids=None):
        """用户拉新统计"""
        try:
            command = """
            SELECT FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d') AS create_time, COUNT(*) AS count
            FROM shu_recommended_users
            WHERE create_time >= :start_time
            AND create_time < :end_time
            AND status = 1
            AND is_deleted = 0
            %s
            GROUP BY FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d')"""

            # 城市经理且推广人员为空
            if 4 == params['role_type'] and not promoter_ids:
                command = command % 'AND referrer_user_id IN (0) '
            # 非城市经理查看所有人
            elif not promoter_ids:
                command = command % ''
            # 城市经理且有推广人员
            else:
                referrer_user_id = 'AND referrer_user_id IN (%s) ' % ','.join(promoter_ids)
                command = command % referrer_user_id

            promote_quality = cursor.query(command, {
                'start_time': params['start_time'],
                'end_time': params['end_time'],
            })
            # 累计
            before_promote_count = 0
            if params['data_type'] == 2:
                command = """
                SELECT COUNT(*) AS count
                FROM shu_recommended_users
                WHERE create_time < :start_time
                AND status = 1
                AND is_deleted = 0
                %s """

                # 城市经理且推广人员为空
                if 4 == params['role_type'] and not promoter_ids:
                    command = command % 'AND referrer_user_id IN (0) '
                # 非城市经理查看所有人
                elif not promoter_ids:
                    command = command % ''
                # 城市经理且有推广人员
                else:
                    referrer_user_id = 'AND referrer_user_id IN (%s) ' % ','.join(promoter_ids)
                    command = command % referrer_user_id

                before_promote = cursor.query_one(command, {
                    'start_time': params['start_time'],
                })
                before_promote_count = before_promote['count'] if before_promote else 0

            return promote_quality if promote_quality else [], before_promote_count

        except Exception as e:
            log.error('用户拉新统计异常: [error: %s]' % e, exc_info=True)

    @staticmethod
    def get_user_behavior(cursor, params, promoter_ids=None):
        """用户行为统计"""
        try:
            # 登录
            if params.get('data_type') == 1:
                command = """
                -- 用户登录
                SELECT FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d') AS create_time, COUNT(*) AS count

                FROM shu_recommended_users
                LEFT JOIN shu_user_stats ON shu_recommended_users.recommended_user_id = shu_user_stats.user_id
                AND shu_user_stats.last_login_time > shu_recommended_users.create_time

                WHERE create_time >= :start_time
                AND create_time < :end_time
                AND is_deleted = 0
                %s
                GROUP BY FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d')
                """
            # 发货
            elif params.get('data_type') == 2:
                command = """ 
                -- 用户发货
                SELECT FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d') AS create_time, COUNT(*) AS count

                FROM shu_recommended_users

                WHERE create_time >= :start_time
                AND create_time < :end_time
                AND is_deleted = 0
                %s
                AND (SELECT COUNT(*)
                FROM shf_goods
                WHERE shf_goods.user_id = shu_recommended_users.recommended_user_id
                AND shf_goods.create_time > shu_recommended_users.create_time) > 0
                GROUP BY FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d')
                 """
            # 接单
            elif params.get('data_type') == 3:
                command = """
                -- 用户接单
                SELECT FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d') AS create_time, COUNT(*) AS count

                FROM shu_recommended_users

                WHERE create_time >= :start_time
                AND create_time < :end_time
                AND is_deleted = 0
                %s
                AND (SELECT COUNT(*)
                FROM shb_orders
                WHERE shb_orders.driver_id = shu_recommended_users.recommended_user_id
                AND shb_orders.create_time > shu_recommended_users.create_time) > 0
                GROUP BY FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d')
                 """
            # 完成订单
            elif params.get('data_type') == 4:
                command = """
                -- 用户完成订单
                SELECT FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d') AS create_time, COUNT(*) AS count

                FROM shu_recommended_users

                WHERE create_time >= :start_time
                AND create_time < :end_time
                AND is_deleted = 0
                %s
                AND (
                (SELECT COUNT(*)
                FROM shb_orders
                WHERE shb_orders.driver_id = shu_recommended_users.recommended_user_id
                AND shb_orders.create_time > shu_recommended_users.create_time
                AND shb_orders.`status` = 3) > 0
                OR
                (SELECT COUNT(*)
                FROM shb_orders
                WHERE shb_orders.owner_id = shu_recommended_users.recommended_user_id
                AND shb_orders.create_time > shu_recommended_users.create_time
                AND shb_orders.`status` = 3) > 0)
                GROUP BY FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d')
                """
            else:
                return []

            # 城市经理且推广人员为空
            if 4 == params['role_type'] and not promoter_ids:
                command = command % 'AND referrer_user_id IN (0) '
            # 非城市经理查看所有人
            elif not promoter_ids:
                command = command % ''
            # 城市经理且有推广人员
            else:
                referrer_user_id = 'AND referrer_user_id IN (%s) ' % ','.join(promoter_ids)
                command = command % referrer_user_id

            promote_quality = cursor.query(command, {
                'start_time': params['start_time'],
                'end_time': params['end_time'],
            })

            return promote_quality if promote_quality else []

        except Exception as e:
            log.error('用户行为统计异常: [error: %s]' % e, exc_info=True)

    @staticmethod
    def get_money(cursor, params, promoter_ids=None):
        """用户金额统计"""
        try:
            # 货源总额
            if params.get('data_type') == 1:
                command = """
                -- 用户货源总额
                SELECT FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d') AS create_time, 
                SUM((SELECT SUM(price_expect + price_addition)
                FROM shf_goods
                WHERE shf_goods.user_id = shu_recommended_users.recommended_user_id
                AND shf_goods.create_time > shu_recommended_users.create_time)) AS count

                FROM shu_recommended_users

                WHERE create_time >= :start_time
                AND create_time < :end_time
                AND is_deleted = 0
                %s
                GROUP BY FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d')
                """
            # 订单总额
            elif params.get('data_type') == 2:
                command = """
                -- 用户订单总额
                SELECT FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d') AS create_time, 
                IF(SUM((SELECT SUM(price)
                FROM shb_orders
                WHERE shu_recommended_users.recommended_user_id = shb_orders.driver_id
                AND shb_orders.create_time > shu_recommended_users.create_time)) IS NULL, 0,
                SUM((SELECT SUM(price)
                FROM shb_orders
                WHERE shu_recommended_users.recommended_user_id = shb_orders.driver_id
                AND shb_orders.create_time > shu_recommended_users.create_time))) +
                IF(SUM((SELECT SUM(price)
                FROM shb_orders
                WHERE shu_recommended_users.recommended_user_id = shb_orders.owner_id
                AND shb_orders.create_time > shu_recommended_users.create_time)) IS NULL, 0,
                SUM((SELECT SUM(price)
                FROM shb_orders
                WHERE shu_recommended_users.recommended_user_id = shb_orders.owner_id
                AND shb_orders.create_time > shu_recommended_users.create_time))) AS count

                FROM shu_recommended_users

                WHERE create_time >= :start_time
                AND create_time < :end_time
                AND is_deleted = 0
                %s
                GROUP BY FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d')
                """
            # 实际完成总额
            elif params.get('data_type') == 3:
                command = """
                -- 用户订单完成总额
                SELECT FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d') AS create_time, 
                IF(SUM((SELECT SUM(price)
                FROM shb_orders
                WHERE shu_recommended_users.recommended_user_id = shb_orders.driver_id
                AND shb_orders.create_time > shu_recommended_users.create_time
                AND shb_orders.`status` = 3)) IS NULL, 0,
                SUM((SELECT SUM(price)
                FROM shb_orders
                WHERE shu_recommended_users.recommended_user_id = shb_orders.driver_id
                AND shb_orders.create_time > shu_recommended_users.create_time
                AND shb_orders.`status` = 3))) +
                IF(SUM((SELECT SUM(price)
                FROM shb_orders
                WHERE shu_recommended_users.recommended_user_id = shb_orders.owner_id
                AND shb_orders.create_time > shu_recommended_users.create_time
                AND shb_orders.`status` = 3)) IS NULL, 0,
                SUM((SELECT SUM(price)
                FROM shb_orders
                WHERE shu_recommended_users.recommended_user_id = shb_orders.owner_id
                AND shb_orders.create_time > shu_recommended_users.create_time
                AND shb_orders.`status` = 3))) AS count

                FROM shu_recommended_users

                WHERE create_time >= :start_time
                AND create_time < :end_time
                AND is_deleted = 0
                %s
                GROUP BY FROM_UNIXTIME(create_time, '%%%%Y-%%%%m-%%%%d')
                """
            else:
                return []

            # 城市经理且推广人员为空
            if 4 == params['role_type'] and not promoter_ids:
                command = command % 'AND referrer_user_id IN (0) '
            # 非城市经理查看所有人
            elif not promoter_ids:
                command = command % ''
            # 城市经理且有推广人员
            else:
                referrer_user_id = 'AND referrer_user_id IN (%s) ' % ','.join(promoter_ids)
                command = command % referrer_user_id

            promote_quality = cursor.query(command, {
                'start_time': params['start_time'],
                'end_time': params['end_time'],
            })

            for i in promote_quality:
                if not i['count']:
                    i['count'] = 0

            return promote_quality if promote_quality else []

        except Exception as e:
            log.error('用户金额统计异常: [error: %s]' % e, exc_info=True)

