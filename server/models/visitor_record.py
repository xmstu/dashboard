# -*- coding: utf-8 -*-

from server import log


class VisitorRecordModel(object):
    @staticmethod
    def add_record(cursor, params):
        """添加访客记录"""
        command = '''
        INSERT INTO tb_inf_user_visit(user_id, user_name, user_role, url, ip, user_agent, visit_time)
        VALUES (:user_id, :user_name, :user_role, :url, :ip, :user_agent, :visit_time)'''

        result = cursor.insert(command, params)
        return result