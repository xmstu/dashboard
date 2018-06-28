from server import log


class FreshOwnerModel(object):

    @staticmethod
    def get_fresh_owner_id(cursor):
        try:
            # 先找出所有发货小于3的user_id
            good_sql = """
                SELECT shf_goods.user_id FROM shf_goods GROUP BY shf_goods.user_id HAVING COUNT( 1 ) < 3
            """
            good_user_ret = cursor.query(good_sql)
            good_ret_list = [str(i['user_id']) for i in good_user_ret]
            # 再找出订单列表中发货小于3的owner_id
            order_sql = """SELECT DISTINCT owner_id FROM shb_orders WHERE owner_id IN ( %s )""" % ','.join(good_ret_list)
            log.debug('获取新货主SQL语句：[sql: %s]' % order_sql)
            order_owner_ret = cursor.query(order_sql)
            ret = [str(i['owner_id']) for i in order_owner_ret]
            return ret
        except Exception as e:
            log.error('Error:{}'.format(e))

        return ['0']


class FreshDriverModel(object):

    @staticmethod
    def get_fresh_driver_id(cursor):
        try:
            sql = """
                    SELECT
                        driver_id
                    FROM
                        shb_orders 
                    GROUP BY
                        driver_id 
                    HAVING
                        COUNT( 1 ) < 3
                    """
            ret = cursor.query(sql)

            ret = [str(i['driver_id']) for i in ret]

            return ret
        except Exception as e:
            log.error('Error:{}'.format(e))

        return ['0']
