# -*- coding: utf-8 -*-

from server import log

class RegionsModel(object):
    @staticmethod
    def get_three_area(cursor, code):
        try:
            command = """
            SELECT region.*, shm_regions.parent_id AS first_code
            FROM shm_regions
            INNER JOIN (SELECT id AS third_code, parent_id AS second_code
            FROM shm_regions
            WHERE id = :code) AS region ON shm_regions.id = region.second_code
            """
            result = cursor.query_one(command, {
                'code': code
            })

            return result if result else {}

        except Exception as e:
            log.warn('获取三级地区失败: [error: %s]' % (e,), exc_info=True)

    @staticmethod
    def get_user_region(cursor, user_id):
        """获取区镇合伙人查询地区"""
        try:
            command = """
            SELECT
                shd_supplier_areas.region_id AS region_id,
                shm_regions.full_short_name
            
            FROM shd_supplier_areas
            LEFT JOIN shm_regions ON shm_regions.id = shd_supplier_areas.region_id
            LEFT JOIN shd_suppliers ON shd_suppliers.id = shd_supplier_areas.supplier_id
            WHERE shd_suppliers.user_id = :user_id AND shd_suppliers.is_deleted = 0
            """
            result = cursor.query(command, {
                'user_id': user_id
            })

            return result if result else []

        except Exception as e:
            log.warn('获取管理员查询地区失败: [error: %s]' % (e,), exc_info=True)

    @staticmethod
    def get_region_by_code(cursor, code):
        """获取地区全称"""
        try:
            command = """
            SELECT `code`, full_short_name
            FROM shm_regions
            WHERE `code` = :code AND is_deleted = 0
            """
            result = cursor.query_one(command, {
                'code': code
            })

            return result if result else {}

        except Exception as e:
            log.warn('获取地区全称失败: [error: %s]' % (e,), exc_info=True)

    @staticmethod
    def get_admin_region(cursor):
        """内部用户地区"""
        command = """
        SELECT id, full_short_name
        FROM shm_regions
        WHERE `level` = 1
        """
        result = cursor.query(command)

        log.info('获取内部用户地区')
        return result if result else []