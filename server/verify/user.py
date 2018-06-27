# -*- coding: utf-8 -*-

import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.status import HTTPStatus, make_result, APIStatus
from server.meta.session_operation import sessionOperationClass
from server.cache_data import init_regions
from server.utils.extend import compare_time


class UserStatistic(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            # 校验参数
            start_time = int(params.get('start_time')) if params.get('start_time') else time.time() - 8 * 60 * 60 * 24
            end_time = int(params.get('end_time')) if params.get('end_time') else time.time() - 60 * 60 * 24
            periods = int(params.get('periods')) if params.get('periods') else 2
            user_type = int(params.get('user_type')) if params.get('user_type') else 1
            role_type = int(params.get('role_type')) if params.get('role_type') else 0
            region_id = int(params.get('region_id')) if params.get('region_id') else 0
            is_auth = int(params.get('is_auth')) if params.get('is_auth') else 0

            if start_time and end_time:
                if start_time <= end_time:
                    pass
                else:
                    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间参数有误'))
            elif not start_time and not end_time:
                pass
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间参数有误'))

            # 当前权限下所有地区
            role, locations_id = sessionOperationClass.get_locations()
            # 选择地区或者非管理员全部地区
            if role in (2, 3, 4) and not region_id:
                region_id = set("'"+init_regions.get_city_level(i)['short_name']+"'" for i in locations_id if init_regions.get_city_level(i)['short_name'])
            elif region_id:
                region_id = "'"+init_regions.get_city_level(region_id)['short_name']+"'"

            params = {
                'start_time': start_time,
                'end_time': end_time,
                'periods': periods,
                'user_type': user_type,
                'role_type': role_type,
                'region_id': region_id,
                'is_auth': is_auth
            }

            return Response(params=params)
        except Exception as e:
            log.warn('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求参数非法'))


class UserList(object):

    @staticmethod
    @make_decorator
    def check_params(page, limit, params):

        try:
            user_name = params.get('user_name') if params.get('user_name') else ''
            mobile = params.get('mobile') if params.get('mobile') else ''
            reference_mobile = params.get('reference_mobile') if params.get('reference_mobile') else ''
            download_ch = params.get('download_ch') if params.get('download_ch') else ''
            from_channel = params.get('from_channel') if params.get('from_channel') else ''

            is_referenced = int(params.get('is_referenced')) if params.get('is_referenced') else 0

            home_station_province = int(params.get('home_station_province')) if params.get('home_station_province') else 0
            home_station_city = int(params.get('home_station_city')) if params.get('home_station_city') else 0
            home_station_county = int(params.get('home_station_county')) if params.get('home_station_county') else 0

            role_type = int(params.get('role_type')) if params.get('role_type') else 0
            role_auth = int(params.get('role_auth')) if params.get('role_auth') else 0
            is_actived = int(params.get('is_actived')) if params.get('is_actived') else 0
            is_used = int(params.get('is_used')) if params.get('is_used') else 0
            is_car_sticker = int(params.get('is_car_sticker')) if params.get('is_car_sticker') else 0

            last_login_start_time = int(params.get('last_login_start_time')) if params.get(
                'last_login_start_time') else 0
            last_login_end_time = int(params.get('last_login_end_time')) if params.get('last_login_end_time') else 0

            register_start_time = int(params.get('register_start_time')) if params.get('register_start_time') else 0
            register_end_time = int(params.get('register_end_time')) if params.get('register_end_time') else 0

            region_id = None

            # 检验最后登陆时间
            if not compare_time(last_login_start_time, last_login_end_time):
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='最后登录时间有误'))

            # 检验注册时间
            if not compare_time(register_start_time, register_end_time):
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='注册时间有误'))

            # 当前权限下所有地区
            role, locations_id = sessionOperationClass.get_locations()
            if role in (2, 3, 4) and not region_id:
                region_id = locations_id

            params = {
                'user_name': user_name,
                'mobile': mobile,
                'reference_mobile': reference_mobile,
                'download_ch': download_ch,
                'from_channel': from_channel,
                'is_referenced': is_referenced,
                'home_station_province': home_station_province,
                'home_station_city': home_station_city,
                'home_station_county': home_station_county,
                'role_type': role_type,
                'role_auth': role_auth,
                'is_actived': is_actived,
                'is_used': is_used,
                'is_car_sticker': is_car_sticker,
                'last_login_start_time': last_login_start_time,
                'last_login_end_time': last_login_end_time,
                'register_start_time': register_start_time,
                'register_end_time': register_end_time,
                'region_id': region_id
            }

            log.info("Response:{}".format(params))

            return Response(page=page, limit=limit, params=params)

        except Exception as e:
            log.info("Error:{}".format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求参数有误'))
