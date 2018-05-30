# -*- coding: utf-8 -*-


class PromoteEffetList(object):
    @staticmethod
    def get_promote_effet_list(cursor, page, limit, params):

        command = """"""

        fileds = """"""

        # TODO 语句需要优化
        command += """
            ORDER BY
            unknown.last_login_time DESC 
            LIMIT %s,
            %s""" % ((page-1)*limit, limit)

        promote_effet_list = cursor.query(command)

        return promote_effet_list if promote_effet_list else None