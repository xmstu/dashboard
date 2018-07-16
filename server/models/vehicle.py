# -*- coding: utf-8 -*-

from server.logger import log

class VehicleModel(object):
    @staticmethod
    def get_vehicle_length_name(cursor, length_id, user_id):
        """获取车长名称"""
        try:
            command = '''
            SELECT
            (SELECT COUNT(1) FROM shb_orders WHERE driver_id = shu_users.id) AS order_count,
            (SELECT COUNT(1) FROM shb_orders WHERE driver_id = shu_users.id AND shb_orders.`status` = 3) AS order_finished,
            (SELECT COUNT(1) FROM shb_orders WHERE driver_id = shu_users.id AND shb_orders.`status` = -1) AS order_cancel,
            (SELECT `name` FROM shm_dictionary_items WHERE id = :length_id) AS `name`,
            (SELECT `value` FROM shm_dictionary_items WHERE id = :length_id) AS `value`
            FROM shu_users
            WHERE id = :user_id '''

            result = cursor.query_one(command, {
                'user_id': user_id,
                'length_id': length_id
            })

            return result if result else {}
        except Exception as e:
            log.error('获取车长名称出错: [length_id: %s][e: %s]' % (length_id, e), exc_info=True)

    @staticmethod
    def get_user_order_vehicle_data(cursor, user_id, length_id):
        """获取用户订单和车型数据"""
        try:
            command = ''''''

        except Exception as e:
            log.error('获取用户订单和车型数据出错: [user_id : %s][length_id: %s][e : %s]' % (user_id, length_id, e), exc_info=True)