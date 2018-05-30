# -*- coding: utf-8 -*-


class PromoteEffetList(object):
    @staticmethod
    def get_promote_effet_list(cursor, page, limit, params):

        # 查询字段
        fileds = """"""

        command = """"""

        # TODO 语句需要优化
        # 分页
        command += """
            ORDER BY
            unknown.last_login_time DESC 
            LIMIT %s,
            %s""" % ((page - 1) * limit, limit)

        promote_effet_detail = cursor.query(command)

        promote_effet_list = {'promote_effet_detail': promote_effet_detail, 'count': None}

        return promote_effet_list if promote_effet_list else None
