from server import log


class FreshOwnerModel(object):

    @staticmethod
    def get_fresh_owner_id(cursor):
        try:
            sql = """
                SELECT
                    shf_goods.user_id
                FROM
                    shf_goods
                    INNER JOIN shb_orders so ON shf_goods.user_id = so.owner_id
                    GROUP BY
                    shf_goods.user_id
                    HAVING
                    COUNT(1) < 3
                """
            log.debug('获取新货主SQL语句：[sql: %s]' % sql)
            ret = cursor.query(sql)
            return ret
        except Exception as e:
            log.error('Error:{}'.format(e))

        return []
