# -*- coding: utf-8 -*-
from flask import abort

from server import log
from server.meta.session_operation import sessionOperationClass
from server.status import HTTPStatus, make_result, APIStatus


class Login(object):
    @staticmethod
    def get_user_by_admin(cursor, user_name, password):
        """后台用户登录"""
        command = """
        SELECT
            tb_inf_admins.id,
            account,
            user_name,
            avatar_url,
            tb_inf_roles.id role_id,
            tb_inf_roles.`name` role,
            GROUP_CONCAT(DISTINCT region_id) region_id,
            GROUP_CONCAT(DISTINCT path) path,
            GROUP_CONCAT(DISTINCT tb_inf_menus.`name`) menu_name
        FROM
            tb_inf_admins
            INNER JOIN tb_inf_admin_roles ON tb_inf_admin_roles.admin_id = tb_inf_admins.id AND tb_inf_admin_roles.is_deleted = 0
            INNER JOIN tb_inf_roles ON tb_inf_roles.id = tb_inf_admin_roles.role_id AND tb_inf_roles.is_deleted = 0
            INNER JOIN tb_inf_role_pages ON tb_inf_role_pages.role_id = tb_inf_roles.id AND tb_inf_role_pages.is_deleted = 0
            INNER JOIN tb_inf_pages ON tb_inf_pages.id = tb_inf_role_pages.page_id AND tb_inf_pages.is_deleted = 0
            INNER JOIN tb_inf_menus ON tb_inf_menus.id = tb_inf_pages.menu_id AND tb_inf_menus.is_deleted = 0
        WHERE
            tb_inf_admins.is_deleted = 0
            AND user_name = :user_name
            AND `password` = :password
        GROUP BY
            role_id
        """
        result = cursor.query(command, {'user_name': user_name, 'password': password})
        user_session = []
        for detail in result:
            user_session.append({
                'role': detail['role'],
                'role_id': detail['role_id'],
                'locations': detail['region_id'],
                'path': detail['path'],
                'menu_name': detail['menu_name']
            })

        if not sessionOperationClass.set_session('user_session', user_session):
            abort(HTTPStatus.InternalServerError,
                  **make_result(status=APIStatus.InternalServerError, msg='添加session失败'))

        result = result[0]
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
