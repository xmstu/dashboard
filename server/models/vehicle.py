# -*- coding: utf-8 -*-

from server.logger import log

class VehicleModel(object):
    @staticmethod
    def get_vehicle_length_name(cursor, length_id):
        """获取车长名称"""
        try:
            command = '''
            SELECT `name`
            FROM shm_dictionary_items
            WHERE id = :length_id'''
            result = cursor.query_one(command, {
                'length_id': length_id
            })
            return result['name'] if result else ''
        except Exception as e:
            log.error('获取车长名称出错: [length_id: %s][e: %s]' % (length_id, e), exc_info=True)