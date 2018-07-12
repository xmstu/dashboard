# -*- coding: utf-8 -*-

class VehicleModel(object):
    @staticmethod
    def get_vehicle_length_name(cursor, length_id):
        """获取车长名称"""
        command = '''
        SELECT `name`
        FROM shm_dictionary_items
        WHERE id = :length_id'''

        result = cursor.query_one(command)
        return result['name'] if result else ''