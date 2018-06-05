# coding=utf-8

from server import init_regions


def to_address(province_id, city_id, county_id):
    province = init_regions.get(province_id, {'name': ''})
    city = init_regions.get(city_id, {'name': ''})
    county = init_regions.get(county_id, {'name': ''})
    return province['name'] + city['name'] + county['name']


def to_province(province_id):
    return init_regions.get(int(province_id), {'name': ''}).get('name')


def to_city(city_id):
    return init_regions.get(int(city_id), {'name': ''}).get('name')


def to_county(county_id):
    return init_regions.get(int(county_id), {'name': ''}).get('name')


def to_town(town_id):
    return init_regions.get(int(town_id), {'name': ''}).get('name')
