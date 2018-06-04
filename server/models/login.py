# -*- coding: utf-8 -*-
from server import log


class Login(object):
    @staticmethod
    def get_user_by_admin(cursor, user_name, password):
        """后台用户登录"""
        command = """
        SELECT sha_users.id,
        sha_user_profiles.mobile,
        sha_user_profiles.real_name AS user_name,
        '' AS avatar_url
        
        FROM sha_users
        LEFT JOIN sha_user_profiles ON sha_users.id = sha_user_profiles.user_id
        WHERE user_name = :user_name AND `password` = :password AND sha_users.is_deleted = 0
        """
        result = cursor.query_one(command, {'user_name': user_name, 'password': password})

        log.info('获取后台登录用户sql参数: [user_name: %s][password: %s]' % (user_name, password))
        return result if result else None

    @staticmethod
    def get_user_by_user(cursor, user_name, password):
        """外部用户登录"""
        command = """
            SELECT shu_users.id,
            shu_users.mobile,
            shu_user_profiles.user_name,
            shu_user_profiles.avatar_url
            
            FROM shu_users
            LEFT JOIN shu_user_profiles ON shu_users.id = shu_user_profiles.user_id
            WHERE `mobile` = :mobile AND `password` = :password AND shu_users.is_deleted = 0
        """
        result = cursor.query_one(command, {'mobile': user_name, 'password': password})

        log.info('获取外部登录用户sql参数: [user_name: %s][password: %s]' % ( user_name, password))
        return result if result else None
