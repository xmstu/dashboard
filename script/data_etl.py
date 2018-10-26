# -*- coding: utf-8 -*-

import datetime
import time

from server.cache_data import init_regions as regions
from server.database import db
from server.logger import log
from server.models.data_etl import daUserModel, UserInfoModel


def data_etl_main():
    """数据导入"""
    log.info('同步数据平台用户数据开始,当前时间是: %s' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    try:
        statistics_date = daUserModel.is_update(db.read_bi)
        # 清除数据
        result = False
        if not statistics_date:
            result = delete_user_info()
        else:
            statistics_date = datetime.datetime.strptime(statistics_date, "%Y-%m-%d")
            now = datetime.datetime.now()
            # 清除数据
            if (now - statistics_date).seconds > 0:
                result = delete_user_info()
        if result:
            # 记录当天登录过用户
            add_last_login_user()
            # 获取用户总数
            all_count = get_all_user_count()
            # 分片查询, 省内存
            for i in range(0, all_count, 10000):
                # 获取运力车型
                transport_vehicles = get_transport_vehicles(db.read_db, i)
                # 车型去重
                for j in transport_vehicles:
                    j['vehicle_length_id'] = ','.join(set(str(j['vehicle_length_id']).split(',')))
                # 写入运力车型数据
                insert_transport_vehicles(db.write_bi, transport_vehicles)
                user_info, user_area = select_user_info(i)
                # 计算用户常驻地
                user_arr = calculate_region(user_area)
                # 写入数据
                insert_data(user_info, user_arr)
            log.info('同步数据平台用户数据结束,当前时间是: %s' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    except Exception as e:
        log.error('同步用户信息失败: [error: %s]' % e, exc_info=True)


def delete_user_info():
    """清除数据"""
    try:
        daUserModel.delete_user_table(db.write_bi)
        return True
    except Exception as e:
        log.error('清除数据失败: [error: %s]' % e, exc_info=True)


def add_last_login_user():
    '''记录当天登录过用户'''
    try:
        # 记录当天登录过用户
        last_login_user = UserInfoModel.get_last_login_user(db.read_db)
        if last_login_user:
            last_login_user = [{'user_id': i['user_id'],
                                'last_login_time': i.get('last_login_time', 0),
                                'keep_login_days': i.get('keep_login_days', 0),
                                'statistics_date': i.get('statistics_date', '0000-00-00')
                                } for i in last_login_user if i.get('user_id')]
            UserInfoModel.add_last_login_user(db.write_bi, last_login_user)
    except Exception as e:
        log.error('记录当天登录过用户异常: [error: %s]' % e, exc_info=True)


def get_transport_vehicles(cursor, counts):
    '''记录运力车型'''
    try:
        return UserInfoModel.get_transport_vehicles(cursor, counts)
    except Exception as e:
        log.error('记录运力车型异常: [error: %s]' % e, exc_info=True)


def get_all_user_count():
    '''获取用户总数'''
    try:
        return UserInfoModel.get_user_count(db.read_db)
    except Exception as e:
        log.error('获取用户总数异常: [error: %s]' % e, exc_info=True)


def select_user_info(counts):
    """查询用户"""
    try:
        user_info = UserInfoModel.get_user_detail(db.read_db, counts)
        for j in user_info:
            if j['vehicle_length_id']:
                j['vehicle_length_id'] = ','.join([str(i) for i in set(j['vehicle_length_id'].split(','))])
            else:
                j['vehicle_length_id'] = ''
        user_area = UserInfoModel.geet_user_resident(db.read_db, counts)
        return user_info, user_area
    except Exception as e:
        log.warn('查询用户失败: [error: %s]' % e, exc_info=True)


def calculate_region(user_area):
    """计算用户常驻地"""
    try:
        user_arr = {}
        for i in user_area:
            user_arr[i['id']] = {'prov': 0, 'city': 0, 'county': 0, 'town': 0}
            # 车辆
            if i['vehicles_prov'] not in ('0', None) or i['vehicles_city'] not in ('0', None) or i['vehicles_county'] not in ('0', None) or i['vehicles_town'] not in ('0', None):
                if i['vehicles_town']:
                    town = i['vehicles_town'].split(',')
                    most_town = sorted([(j, town.count(j)) for j in set(town)], key=lambda x: x[1], reverse=True)
                    user_arr[i['id']]['town'] = 0
                    for town_id, town_count in most_town:
                        if town_id:
                            user_arr[i['id']]['town'] = int(town_id)
                            break
                if i['vehicles_county']:
                    county = i['vehicles_county'].split(',')
                    most_county = sorted([(j, county.count(j)) for j in set(county)], key=lambda x: x[1], reverse=True)
                    user_arr[i['id']]['county'] = 0
                    for county_id, county_count in most_county:
                        if county_id and user_arr[i['id']]['town'] and county_id[:2] == str(user_arr[i['id']]['town'])[:2]:
                            user_arr[i['id']]['county'] = int(county_id)
                            break
                        elif county_id and user_arr[i['id']]['town'] and len(str(user_arr[i['id']]['town'])) > 9:
                            user_arr[i['id']]['county'] = int(county_id)
                            break
                        else:
                            continue
                if i['vehicles_city']:
                    city = i['vehicles_city'].split(',')
                    most_city = sorted([(j, city.count(j)) for j in set(city)], key=lambda x: x[1], reverse=True)
                    user_arr[i['id']]['city'] = 0
                    for city_id, city_count in most_city:
                        if city_id and user_arr[i['id']]['county'] and city_id[:2] == str(user_arr[i['id']]['county'])[:2]:
                            user_arr[i['id']]['city'] = int(city_id)
                            break
                if i['vehicles_prov']:
                    prov = i['vehicles_prov'].split(',')
                    most_prov = sorted([(j, prov.count(j)) for j in set(prov)], key=lambda x: x[1], reverse=True)
                    user_arr[i['id']]['prov'] = 0
                    for prov_id, prov_count in most_prov:
                        if prov_id and user_arr[i['id']]['city'] and prov_id[:2] == str(user_arr[i['id']]['city'])[:2]:
                            user_arr[i['id']]['prov'] = int(prov_id)
                            break

            # 货源
            elif i['goods_prov'] not in ('0', None) or i['goods_city'] not in ('0', None) or i['goods_county'] not in ('0', None) or i['goods_town'] not in ('0', None):
                if i['goods_town'] not in ('0', None):
                    town = i['goods_town'].split(',')
                    most_town = sorted([(j, town.count(j)) for j in set(town)], key=lambda x: x[1], reverse=True)
                    user_arr[i['id']]['town'] = 0
                    for town_id, town_count in most_town:
                        if town_id:
                            user_arr[i['id']]['town'] = int(town_id)
                            break
                if i['goods_county'] not in ('0', None):
                    county = i['goods_county'].split(',')
                    most_county = sorted([(j, county.count(j)) for j in set(county)], key=lambda x: x[1], reverse=True)
                    user_arr[i['id']]['county'] = 0
                    for county_id, county_count in most_county:
                        if county_id and user_arr[i['id']]['town'] and county_id[:2] == str(user_arr[i['id']]['town'])[:2]:
                            user_arr[i['id']]['county'] = int(county_id)
                            break
                        elif county_id and user_arr[i['id']]['town'] and len(str(user_arr[i['id']]['town'])) > 9:
                            user_arr[i['id']]['county'] = int(county_id)
                            break
                        else:
                            continue

                if i['goods_city'] not in ('0', None):
                    city = i['goods_city'].split(',')
                    most_city = sorted([(j, city.count(j)) for j in set(city)], key=lambda x: x[1], reverse=True)
                    user_arr[i['id']]['city'] = 0
                    for city_id, city_count in most_city:
                        if city_id and user_arr[i['id']]['county'] and city_id[:2] == str(user_arr[i['id']]['county'])[:2]:
                            user_arr[i['id']]['city'] = int(city_id)
                            break
                if i['goods_prov'] not in ('0', None):
                    prov = i['goods_prov'].split(',')
                    most_prov = sorted([(j, prov.count(j)) for j in set(prov)], key=lambda x: x[1], reverse=True)
                    user_arr[i['id']]['prov'] = 0
                    for prov_id, prov_count in most_prov:
                        if prov_id and user_arr[i['id']]['city'] and prov_id[:2] == str(user_arr[i['id']]['city'])[:2]:
                            user_arr[i['id']]['prov'] = int(prov_id)
                            break

            # 订单
            elif i['order_prov'] not in ('0', None) or i['order_city'] not in ('0', None) or i['order_county'] not in ('0', None) or i['order_town'] not in ('0', None):
                if i['order_town'] not in ('0', None):
                    town = i['order_town'].split(',')
                    most_town = sorted([(j, town.count(j)) for j in set(town)], key=lambda x: x[1], reverse=True)
                    user_arr[i['id']]['town'] = 0
                    for town_id, town_count in most_town:
                        if town_id:
                            user_arr[i['id']]['town'] = int(town_id)
                            break
                if i['order_county'] not in ('0', None):
                    county = i['order_county'].split(',')
                    most_county = sorted([(j, county.count(j)) for j in set(county)], key=lambda x: x[1], reverse=True)
                    user_arr[i['id']]['county'] = 0
                    for county_id, county_count in most_county:
                        if county_id and user_arr[i['id']]['town'] and county_id[:2] == str(user_arr[i['id']]['town'])[:2]:
                            user_arr[i['id']]['county'] = int(county_id)
                            break
                        elif county_id and user_arr[i['id']]['town'] and len(str(user_arr[i['id']]['town'])) > 9:
                            user_arr[i['id']]['county'] = int(county_id)
                            break
                        else:
                            continue
                if i['order_city'] not in ('0', None):
                    city = i['order_city'].split(',')
                    most_city = sorted([(j, city.count(j)) for j in set(city)], key=lambda x: x[1], reverse=True)
                    user_arr[i['id']]['city'] = 0
                    for city_id, city_count in most_city:
                        if city_id and user_arr[i['id']]['county'] and city_id[:2] == str(user_arr[i['id']]['county'])[:2]:
                            user_arr[i['id']]['city'] = int(city_id)
                            break
                if i['order_prov'] not in ('0', None):
                    prov = i['order_prov'].split(',')
                    most_prov = sorted([(j, prov.count(j)) for j in set(prov)], key=lambda x: x[1], reverse=True)
                    user_arr[i['id']]['prov'] = 0
                    for prov_id, prov_count in most_prov:
                        if prov_id and user_arr[i['id']]['city'] and prov_id[:2] == str(user_arr[i['id']]['city'])[:2]:
                            user_arr[i['id']]['prov'] = int(prov_id)
                            break
            # 手机归属地
            else:
                if i['region_id']:
                    print("获取手机归属地城市: [user_id:{}, city_region_id: {}]".format(i["id"], i["region_id"]))
                    result = regions.get_level_to_prov(i['region_id'])
                    user_arr[i['id']]['prov'] = result['id']
                    user_arr[i['id']]['city'] = i['region_id']
        return user_arr
    except Exception as e:
        log.warn('计算用户常驻地失败: [error: %s]' % e, exc_info=True)


def insert_data(user_info, user_arr):
    """写入数据"""
    try:
        # 整理数据
        result = []
        for i in user_info:
            area = user_arr.get(i['user_id'], {'prov': 0, 'city': 0, 'county': 0, 'town': 0})
            result.append({
                'user_id': i['user_id'],
                'user_name': i['user_name'],
                'mobile': i['mobile'],
                'user_type': i['user_type'],
                'goods_auth': i['goods_auth'] if i['goods_auth'] else 0,
                'driver_auth': i['driver_auth'] if i['driver_auth'] else 0,
                'company_auth': i['company_auth'] if i['company_auth'] else 0,
                'goods_count_SH': i['goods_count_SH'],
                'goods_count_LH': i['goods_count_LH'],
                'order_count_SH': i['order_count_SH'],
                'order_count_LH': i['order_count_LH'],
                'order_finished_count_SH_online': i['order_finished_count_SH_online'],
                'order_finished_count_SH_unline': i['order_finished_count_SH_unline'],
                'order_finished_count_LH_online': i['order_finished_count_LH_online'],
                'order_finished_count_LH_unline': i['order_finished_count_LH_unline'],
                'goods_price_SH': i['goods_price_SH'] if i['goods_price_SH'] else 0,
                'goods_price_LH': i['goods_price_LH'] if i['goods_price_LH'] else 0,
                'order_price_SH': i['order_price_SH'] if i['order_price_SH'] else 0,
                'order_price_LH': i['order_price_LH'] if i['order_price_LH'] else 0,
                'order_over_price_SH_online': i['order_over_price_SH_online'] if i['order_over_price_SH_online'] else 0,
                'order_over_price_SH_unline': i['order_over_price_SH_unline'] if i['order_over_price_SH_unline'] else 0,
                'order_over_price_LH_online': i['order_over_price_LH_online'] if i['order_over_price_LH_online'] else 0,
                'order_over_price_LH_unline': i['order_over_price_LH_unline'] if i['order_over_price_LH_unline'] else 0,
                'download_channel': i['download_channel'],
                'from_channel': i['from_channel'],
                'from_province_id': area['prov'],
                'from_city_id': area['city'],
                'from_county_id': area['county'],
                'from_town_id': area['town'],
                'referrer_mobile': i['referrer_mobile'] if i['referrer_mobile'] else '',
                'last_login_time': i['last_login_time'],
                'keep_login_days': i['keep_login_days'],
                'is_sticker': i['is_sticker'],
                'recommended_status': i['recommended_status'],
                'vehicle_length_id': i['vehicle_length_id'],
                'create_time': i['create_time'],
                'statistics_date': int(time.time())
            })
        daUserModel.insert_data(db.write_bi, result)
        log.debug('写入数据库条数: [count: %s]' % len(result))
    except Exception as e:
        log.warn('写入数据失败: [error: %s]' % e, exc_info=True)


def insert_transport_vehicles(cursor, transport_vehicles):
    """写入运力车型数据"""
    try:
        # 整理数据
        result = []
        for i in transport_vehicles:
            result.append({
                'user_id': i['user_id'],
                'from_province_id': i['from_province_id'],
                'from_city_id': i['from_city_id'],
                'from_county_id': i['from_county_id'],
                'from_town_id': i['from_town_id'],
                'to_province_id': i['to_province_id'],
                'to_city_id': i['to_city_id'],
                'to_county_id': i['to_county_id'],
                'to_town_id': i['to_town_id'],
                'vehicle_length_id': i['vehicle_length_id'],
                'create_time': i['create_time'],
                'statistics_date': time.strftime('%Y-%m-%d', time.localtime())
            })
        if not result:
            return
        daUserModel.insert_transport_vehicles(cursor, result)

    except Exception as e:
        log.warn('写入数据失败: [error: %s]' % e, exc_info=True)
