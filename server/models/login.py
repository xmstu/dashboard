# -*- coding: utf-8 -*-
from server import log


class Login(object):

    @staticmethod
    def get_user(cursor, user_name, password):
        result = cursor.query_one("""
                                  SELECT *
                                  FROM shu_users
                                  WHERE `mobile` = :mobile AND `password` = :password AND is_deleted = 0
                                  """, {'mobile': user_name, 'password': password})

        log.info('获取登录用户sql参数: [user_name: %s][password: %s]' % ( user_name, password))
        return result if result else None
