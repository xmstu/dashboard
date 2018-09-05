# -*- coding: utf-8 -*-
from server import log


class Login(object):
    @staticmethod
    def get_user_by_admin(cursor, user_name, password):
        """后台用户登录"""
        # command = """
        # SELECT sha_users.id,
        # sha_user_profiles.mobile,
        # sha_user_profiles.real_name AS user_name,
        # '' AS avatar_url
        #
        # FROM sha_users
        # LEFT JOIN sha_user_profiles ON sha_users.id = sha_user_profiles.user_id
        # WHERE user_name = :user_name AND `password` = :password AND sha_users.is_deleted = 0
        # AND sha_users.id IN (43, 236, 294, 320, 321, 322, 324)
        # """
        command = """
        SELECT
            tb_inf_admins.id,
            account,
            user_name,
            avatar_url,
            GROUP_CONCAT(DISTINCT tb_inf_roles.`name`) role,
            GROUP_CONCAT(DISTINCT region_id) region_id,
            GROUP_CONCAT(DISTINCT path) path
        FROM
            tb_inf_admins
            INNER JOIN tb_inf_admin_roles ON tb_inf_admin_roles.admin_id = tb_inf_admins.id
            INNER JOIN tb_inf_roles ON tb_inf_roles.id = tb_inf_admin_roles.role_id
            INNER JOIN tb_inf_role_pages ON tb_inf_role_pages.role_id = tb_inf_roles.id
            INNER JOIN tb_inf_pages ON tb_inf_pages.id = tb_inf_role_pages.page_id
        WHERE
            user_name = :user_name
            AND `password` = :password
        GROUP BY tb_inf_admins.id;
        """
        result = cursor.query_one(command, {'user_name': user_name, 'password': password})

        log.info('获取后台登录用户sql参数: [user_name: %s][password: %s]' % (user_name, password))
        return result if result else None

    @staticmethod
    def get_partner_user(cursor, mobile):
        """区镇合伙人登录"""
        command = """
        -- 区镇合伙人
        SELECT shd_suppliers.user_id,  shu_users.mobile, shd_supplier_areas.region_id,
        shu_user_profiles.user_name, shu_user_profiles.avatar_url, '区镇合伙人' AS role
        FROM shd_suppliers
        INNER JOIN shu_users ON shd_suppliers.user_id = shu_users.id AND shu_users.is_deleted = 0
        INNER JOIN shu_user_profiles ON shu_users.id = shu_user_profiles.user_id
        INNER JOIN shd_supplier_areas ON shd_suppliers.id = shd_supplier_areas.supplier_id AND shd_supplier_areas.is_deleted = 0
        WHERE shd_suppliers.is_deleted = 0
        AND shu_users.mobile = :mobile
        UNION
        -- 网点管理员(可见区域同区镇合伙人)
        SELECT node_manager.id, node_manager.mobile, shd_supplier_areas.region_id,
        node_manager.user_name, node_manager.avatar_url, '网点管理员' AS role
        FROM shd_suppliers
        INNER JOIN shd_supplier_areas ON shd_suppliers.id = shd_supplier_areas.supplier_id AND shd_supplier_areas.is_deleted = 0
        INNER JOIN (SELECT shu_users.id, shd_suppliers.user_id, shu_users.mobile, shu_user_profiles.user_name, shu_user_profiles.avatar_url
        FROM shd_supplier_nodes
        INNER JOIN shu_users ON shd_supplier_nodes.manager_user_id = shu_users.id AND shu_users.is_deleted = 0
        INNER JOIN shu_user_profiles ON shu_users.id = shu_user_profiles.user_id
        INNER JOIN shd_suppliers ON shd_suppliers.id = shd_supplier_nodes.supplier_id AND shd_suppliers.is_deleted = 0
        WHERE shd_supplier_nodes.is_deleted = 0
        AND shu_users.mobile = :mobile
        LIMIT 1) AS node_manager ON shd_suppliers.user_id = node_manager.user_id
        WHERE shd_suppliers.is_deleted = 0"""
        result = cursor.query(command, {'mobile': mobile})

        log.info('获取区镇合伙人登录sql参数: [mobile: %s]' % (mobile))
        return result if result else None

    @staticmethod
    def get_user_by_city_manage(cursor, account, password):
        """城市经理登录"""
        try:
            command = """
            SELECT
            id,
            account AS mobile,
            user_name,
            avatar_url,
            region_id
            
            FROM tb_inf_city_manager
            WHERE account = :account AND `password` = :password AND is_deleted = 0
            """
            result = cursor.query_one(command, {'account': account, 'password': password})

            log.debug('获取后台登录用户sql参数: [account: %s][password: %s]' % (account, password))
            return result if result else None
        except Exception as e:
            log.warn('城市经理登录失败 [error: %s]' % e, exc_info=True)