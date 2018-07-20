# -*- coding: utf-8 -*-

from server.logger import log

class VehicleModel(object):
    @staticmethod
    def get_vehicle_length_name(cursor, length_id, user_id):
        """获取车长名称"""
        try:
            command = '''
            SELECT *
            FROM
            (SELECT COUNT(1) AS order_count FROM shb_orders WHERE driver_id = :user_id) AS order_count,
            (SELECT COUNT(1) AS order_finished FROM shb_orders WHERE driver_id = :user_id AND shb_orders.`status` = 3) AS order_finished,
            (SELECT COUNT(1) AS order_cancel FROM shb_orders WHERE driver_id = :user_id AND shb_orders.`status` = -1) AS order_cancel,
            (SELECT `name` AS vehicle_length_id FROM shm_dictionary_items WHERE id = :length_id) AS vehicle_length_id'''
            result = cursor.query_one(command, {
                'user_id': user_id,
                'length_id': length_id
            })
            return result if result else {}
        except Exception as e:
            log.error('获取车长名称出错: [user_id: %s][length_id: %s][e: %s]' % (user_id, length_id, e), exc_info=True)