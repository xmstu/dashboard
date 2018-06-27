# coding=utf-8

from server import cache_data


def to_address(province_id, city_id, county_id):
    province = cache_data.get(province_id, {'name': ''})
    city = cache_data.get(city_id, {'name': ''})
    county = cache_data.get(county_id, {'name': ''})
    return province['name'] + city['name'] + county['name']


def to_province(province_id):
    return cache_data.get(int(province_id), {'name': ''}).get('name')


def to_city(city_id):
    return cache_data.get(int(city_id), {'name': ''}).get('name')


def to_county(county_id):
    return cache_data.get(int(county_id), {'name': ''}).get('name')


def to_town(town_id):
    return cache_data.get(int(town_id), {'name': ''}).get('name')
