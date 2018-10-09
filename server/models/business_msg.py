import re

from server.cache_data import init_regions


class BusinessMsgListModel(object):

    @staticmethod
    def get_msg(cursor, params):

        fields = """
            id,
            content,
            follow_admin_name,
            follow_result,
            FROM_UNIXTIME(create_time, "%Y-%m-%d %H:%I:%S") AS create_time
        """

        fetch_where = """ 1=1 """

        command = """
        SELECT
            {fields}
        FROM
            `x_activity_inputs`
        WHERE
            type = 140
            AND is_deleted = 0
            AND create_time > 1535334977
            AND {fetch_where}
        ORDER BY id DESC
        """

        # 根据权限地区id获取相应的信息
        if params["role_type"] == 4:
            fetch_where += """ 
            AND content REGEXP "装货-省id：%d， 市id：%d" 
            """ % (init_regions.get_parent_id(params['role_regions'][0]), int(params['role_regions'][0]))

        # 先查出区镇合伙人和网点管理员所在城市的所有长期用车信息
        if params["role_type"] in (2, 3):
            parent_city_id = init_regions.get_parent_city(params['role_regions'][0])
            fetch_where += """ 
            AND content REGEXP "装货-省id：%d， 市id：%d" 
            """ % (init_regions.get_parent_id(parent_city_id), parent_city_id)

        count = cursor.query_one(command.format(fields="""COUNT(1) AS count""", fetch_where=fetch_where))["count"]

        command += """ LIMIT %d, %d """ % (params["page"], params["limit"])

        data = cursor.query(command.format(fields=fields, fetch_where=fetch_where))

        # 再将每条信息的地区id通过正则匹配取出来，看地区id是否在地区权限id内
        ret = []
        if params["role_type"] in (2, 3):
            for detail in data:
                content = detail.get('content', '')
                re_ret = re.search('装货-省id：(\d{0,6})， 市id：(\d{0,6})， 区id：(\d{0,6})， 镇id：(\d{0,9})', content)
                county_id, town_id = re_ret.group(3), re_ret.group(4)
                if (county_id in params["role_regions"]) or (town_id in params["role_regions"]):
                    ret.append(detail)
            data = ret
            count = len(ret)

        return {
            "count": count if count else 0,
            "data": data if data else []
        }
