# -*- coding: utf-8 -*-

import time


class MessageSystemModel(object):
    @staticmethod
    def get_sys_msg_list_count(cursor):
        """查询系统消息列表总数"""
        command = """
        SELECT COUNT(*) AS count
        FROM tb_inf_system_message
        """
        result = cursor.query_one(command)
        return result['count'] if result else 0

    @staticmethod
    def get_sys_msg_list(cursor, params):
        """查询系统消息列表"""
        command = """
        SELECT id, title, content, user_id, create_time, update_time, msg_type, is_deleted
        FROM tb_inf_system_message
        ORDER BY update_time DESC
        LIMIT :page, :limit
        """
        result = cursor.query(command, params)
        return result if result else []

    @staticmethod
    def get_sys_msg_by_id(cursor, params):
        """查询系统消息"""
        command = """
        SELECT title, content, user_id, create_time, update_time, msg_type, is_deleted
        FROM tb_inf_system_message
        WHERE id = :msg_id
        """
        result = cursor.query_one(command, params)
        return result if result else {}

    @staticmethod
    def insert_system_message(cursor, params):
        """写入系统消息表"""
        command = """
        INSERT INTO tb_inf_system_message(title, content, user_id, create_time, update_time, msg_type)
        VALUES (:title, :content, :user_id, :create_time, :update_time, :msg_type)
        """
        params['create_time'] = int(time.time())
        params['update_time'] = int(time.time())
        result = cursor.insert(command, params)
        return result

    @staticmethod
    def update_system_message(cursor, params):
        """修改系统消息表"""
        command = """
        UPDATE tb_inf_system_message
        SET title = :title, content = :content, user_id = :user_id, update_time = :update_time, msg_type = :msg_type
        WHERE id = :msg_id
        """
        params['update_time'] = int(time.time())
        result = cursor.update(command, params)
        return result

    @staticmethod
    def delete_system_message(cursor, params):
        """删除系统消息表"""
        command = """
        UPDATE tb_inf_system_message
        SET is_deleted = 1
        WHERE id = :msg_id
        """
        result = cursor.update(command, params)
        return result

    @staticmethod
    def get_system_user(cursor):
        """获取后台用户"""
        command = """
        SELECT
            user_name AS account,
            tb_inf_roles.type AS role
        FROM
            tb_inf_admins
            INNER JOIN tb_inf_admin_roles ON tb_inf_admin_roles.admin_id = tb_inf_admins.id 
            AND tb_inf_admin_roles.is_deleted = 0 
            INNER JOIN tb_inf_roles ON tb_inf_admin_roles.role_id = tb_inf_roles.id
            AND tb_inf_roles.is_deleted = 0 
        WHERE
            tb_inf_admins.is_deleted = 0 
            AND tb_inf_roles.type = 1
        GROUP BY
            tb_inf_admins.id;"""

        result = cursor.query(command)
        return result if result else []

    @staticmethod
    def get_suppliers_user(cursor):
        """获取区镇合伙人"""
        command = """
        SELECT DISTINCT
            user_name AS account,
            2 AS role 
        FROM
            shd_suppliers
            INNER JOIN shu_users ON shd_suppliers.user_id = shu_users.id 
            AND shu_users.is_deleted = 0 
            INNER JOIN shu_user_profiles ON shu_user_profiles.user_id = shu_users.id
            AND shu_user_profiles.is_deleted = 0
        WHERE
            shd_suppliers.is_deleted = 0"""

        result = cursor.query(command)
        return result if result else []

    @staticmethod
    def get_suppliers_user_by_region_id(cursor, region_id):
        """通过region_id获取区镇合伙人"""
        command = """
            SELECT 
                account,
                2 AS role
            FROM
                (
                SELECT
                    DISTINCT user_name AS account,
                    region_id
                FROM
                    shd_supplier_areas ssa
                    INNER JOIN shd_suppliers ss ON ss.id = ssa.supplier_id 
                    INNER JOIN shu_user_profiles ON ss.user_id = shu_user_profiles.user_id 
                    AND shu_user_profiles.is_deleted = 0 
                    INNER JOIN shu_users ON shu_user_profiles.user_id = shu_users.id 
                    AND shu_users.is_deleted = 0 
                WHERE
                    ssa.is_deleted = 0 
                AND ss.is_deleted = 0 
                ) AS a
            WHERE
                region_id IN ({region_id})""".format(region_id=region_id)

        result = cursor.query(command)
        return result if result else []

    @staticmethod
    def get_supplier_nodes(cursor):
        """获取网点管理员"""
        command = """
        SELECT DISTINCT user_name AS account, 3 AS role
        FROM shd_supplier_nodes
        INNER JOIN shu_users ON shd_supplier_nodes.manager_user_id = shu_users.id
        AND shu_users.is_deleted = 0
        INNER JOIN shu_user_profiles ON shu_user_profiles.user_id = shu_users.id
        AND shu_user_profiles.is_deleted = 0
        WHERE shd_supplier_nodes.is_deleted = 0"""

        result = cursor.query(command)
        return result if result else []

    @staticmethod
    def get_supplier_nodes_by_region_id(cursor, region_id):
        """通过region_id获取网点管理员"""
        command = """
            SELECT 
                account,
                3 AS role
            FROM
                (
                SELECT
                    DISTINCT shu_user_profiles.user_name AS account,
                    region_id
                FROM
                    shd_supplier_areas ssa
                    INNER JOIN shd_supplier_nodes ssn ON ssn.supplier_id = ssa.supplier_id 
                    INNER JOIN shu_user_profiles ON ssn.manager_user_id = shu_user_profiles.user_id 
                    AND shu_user_profiles.is_deleted = 0 
                    INNER JOIN shu_users ON shu_user_profiles.user_id = shu_users.id 
                    AND shu_users.is_deleted = 0 
                    AND ssa.is_deleted = 0 
                    AND ssn.is_deleted = 0 
                ) AS a
            WHERE
                region_id IN ({region_id})""".format(region_id=region_id)

        result = cursor.query(command)
        return result if result else []

    @staticmethod
    def get_city_manager(cursor):
        """获取城市经理"""
        command = """
        SELECT
            user_name AS account,
            tb_inf_roles.type AS role
        FROM
            tb_inf_admins
            INNER JOIN tb_inf_admin_roles ON tb_inf_admin_roles.admin_id = tb_inf_admins.id 
            AND tb_inf_admin_roles.is_deleted = 0 
            INNER JOIN tb_inf_roles ON tb_inf_admin_roles.role_id = tb_inf_roles.id
            AND tb_inf_roles.is_deleted = 0 
        WHERE
            tb_inf_admins.is_deleted = 0 
            AND tb_inf_roles.type = 4
        GROUP BY
            tb_inf_admins.id;"""

        result = cursor.query(command)
        return result if result else []

    @staticmethod
    def get_city_manager_by_region_id(cursor, region_id):
        """通过region_id获取城市经理"""
        command = """
        SELECT
            user_name AS account,
            tb_inf_roles.type AS role 
        FROM
            tb_inf_admins
            INNER JOIN tb_inf_admin_roles ON tb_inf_admin_roles.admin_id = tb_inf_admins.id 
            AND tb_inf_admin_roles.is_deleted = 0
            INNER JOIN tb_inf_roles ON tb_inf_admin_roles.role_id = tb_inf_roles.id 
            AND tb_inf_roles.is_deleted = 0 
        WHERE
            tb_inf_admins.is_deleted = 0 
            AND tb_inf_roles.type = 4 
            AND tb_inf_roles.region_id IN ({region_id})
        GROUP BY
            tb_inf_admins.id;
        """.format(region_id=region_id)

        result = cursor.query(command)
        return result if result else []

    @staticmethod
    def insert_user_message(cursor, data):
        """写入用户消息表"""
        command = """
        INSERT INTO tb_inf_user_message(account, role, sys_msg_id, create_time, update_time)
        VALUES (:account, :role, :sys_msg_id, :create_time, :update_time)
        """
        result = cursor.insert(command, data)
        return result

    @staticmethod
    def delete_user_message(cursor, params):
        """删除用户消息表"""
        command = """
        UPDATE tb_inf_user_message
        SET is_deleted = 1
        WHERE sys_msg_id = :msg_id
        """
        result = cursor.update(command, params)
        return result


class MessageUserModel(object):
    @staticmethod
    def get_msg_count(cursor, params):
        """获取用户消息总数"""
        command = """
        SELECT COUNT(*) AS count
        FROM tb_inf_user_message
        WHERE account IN (:account, :user_name)
        AND is_deleted = 0
        """
        result = cursor.query_one(command, params)
        return result['count'] if result else 0

    @staticmethod
    def get_msg_unread_count(cursor, params):
        """获取用户未读消息数"""
        command = """
        SELECT COUNT(*) AS count
        FROM tb_inf_user_message
        WHERE account IN (:account, :user_name)
        AND is_deleted = 0
        AND is_read = 0
        """
        result = cursor.query_one(command, params)
        return result['count'] if result else 0

    @staticmethod
    def get_msg_data(cursor, params):
        """获取用户当前分页消息"""
        command = """
        SELECT tb_inf_user_message.id, is_read, tb_inf_user_message.create_time, tb_inf_system_message.title, tb_inf_system_message.content
        FROM tb_inf_user_message
        INNER JOIN tb_inf_system_message ON tb_inf_user_message.sys_msg_id = tb_inf_system_message.id
        WHERE account IN (:account, :user_name)
        AND tb_inf_user_message.is_deleted = 0
        ORDER BY is_read
        LIMIT :page, :limit"""

        result = cursor.query(command, params)
        return result if result else []

    @staticmethod
    def update_msg_read(cursor, params):
        """修改消息已读状态"""
        command = """
        UPDATE tb_inf_user_message
        SET is_read = 1
        WHERE account = :account AND id = :msg_id
        """

        result = cursor.update(command, params)
        return result
