# coding=utf-8
# author=veficos

from server.logger import log


class Regions(object):
    def __init__(self, region):
        self.region = region

    def to_address(self, province_id, city_id, county_id):
        province = self.region.get(province_id, {'name': ''})
        city = self.region.get(city_id, {'name': ''})
        county = self.region.get(county_id, {'name': ''})
        return province['name'] + city['name'] + county['name']

    def to_province(self, province_id):
        return self.region.get(int(province_id), {'name': ''}).get('name')

    def to_city(self, city_id):
        return self.region.get(int(city_id), {'name': ''}).get('name')

    def to_county(self, county_id):
        return self.region.get(int(county_id), {'name': ''}).get('name')

    def to_town(self, town_id):
        return self.region.get(int(town_id), {'name': ''}).get('name')

    def to_full_short_name(self, region_id):
        return self.region.get(int(region_id), {'full_short_name': ''}).get('full_short_name')

    def to_all_city(self):
        """获取城市级别"""
        return [self.region[i] for i in self.region if self.region[i].get('level', 0) == 2]

    def get_city_level(self, region_id):
        """获取地区code上级到城市"""
        result = self.region.get(int(region_id), {'level': 0})
        if result['level'] <= 3:
            return result['level']
        return self.get_city_level(result['parent_id'])



class InitRegionModel(object):
    @staticmethod
    def get_regions(cursor):
        """ 获取省市区数据 """

        try:
            command = '''SELECT id, `name`, short_name, full_short_name, `level`, parent_id FROM shm_regions WHERE is_deleted = 0'''

            log.debug('获取省市区数据SQL语句：[sql: %s]' % command)

            records = cursor.query(command)

            # log.debug('获取省市区数据SQL语句返回值：[result: %s]' % records)

            return Regions({int(record['id']): record for record in records})

        except Exception as e:
            log.warn('获取省市区数据失败: [error: %s]' % (e,), exc_info=True)

        return Regions({})


    @staticmethod
    def get_province_id(cursor, province_name):
        try:
            command = """
              SELECT id FROM shm_regions WHERE name=:province_name
            """

            log.debug('获取省ID数据SQL语句：[sql: %s]' % command)

            records = cursor.query(command, {
                'province_name': province_name
            })

            log.debug('获取省ID数据SQL语句返回值：[result: %s]' % records)

            return records['id']
        except Exception as e:
            log.warn('获取省ID数据失败: [error: %s]' % (e,), exc_info=True)

        return 0

    @staticmethod
    def get_city_id(cursor, province_name, city_name):
        try:
            command = """
              SELECT citys.id FROM shm_regions AS citys
                INNER JOIN (SELECT * FROM shm_regions) AS provinces ON citys.parent_id=provinces.id AND provinces.name=:province_name
                WHERE citys.name=:city_name
            """

            log.debug('获取市ID数据SQL语句：[sql: %s]' % command)

            records = cursor.query(command, {
                'province_name': province_name,
                'city_name': city_name,
            })

            log.debug('获取市ID数据SQL语句返回值：[result: %s]' % records)

            return records['id']
        except Exception as e:
            log.warn('获取市ID数据失败: [error: %s]' % (e,), exc_info=True)

        return 0

    @staticmethod
    def get_city(cursor):
        """获取城市信息"""
        try:
            command = """
            SELECT id, short_name, center_longitude, center_latitude FROM shm_regions
            WHERE `level` = 2 AND is_deleted = 0 AND center_longitude != 0 AND center_latitude != 0
            """

            log.debug('获取市数据SQL语句：[sql: %s]' % command)

            records = cursor.query(command)

            # log.debug('获取市数据SQL语句返回值：[result: %s]' % records)

            return records
        except Exception as e:
            log.warn('获取市数据失败: [error: %s]' % (e,), exc_info=True)

        return 0

    @staticmethod
    def get_county_id(cursor, province_name, city_name, county_name):
        try:
            command = """
             SELECT countys.id FROM shm_regions AS countys
                INNER JOIN (SELECT * FROM shm_regions) AS citys ON countys.parent_id=citys.id AND citys.name=:city_name
                INNER JOIN (SELECT * FROM shm_regions) AS provinces ON citys.parent_id=provinces.id AND provinces.name=:province_name
                WHERE countys.name=:county_name
            """

            log.debug('获取乡镇ID数据SQL语句：[sql: %s]' % command)

            records = cursor.query(command, {
                'province_name': province_name,
                'city_name': city_name,
                'county_name': county_name,
            })

            log.debug('获取乡镇ID数据SQL语句返回值：[result: %s]' % records)

            return records['id']
        except Exception as e:
            log.warn('获取乡镇ID数据失败: [error: %s]' % (e,), exc_info=True)

        return 0