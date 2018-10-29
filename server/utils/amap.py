# -*- coding: utf-8 -*-

import requests
import simplejson as json
from math import radians, cos, sin, atan, tan, acos


def distance_between_position(from_longitude, from_latitude, to_longitude, to_latitude):
    """ 计算地球两点间距离 """

    try:
        ra = 6378.140  # 赤道半径 (km)
        rb = 6356.755  # 极半径 (km)
        flatten = (ra - rb) / ra  # 地球扁率
        rad_lat_A = radians(from_latitude)
        rad_lng_A = radians(from_longitude)
        rad_lat_B = radians(to_latitude)
        rad_lng_B = radians(to_longitude)
        pA = atan(rb / ra * tan(rad_lat_A))
        pB = atan(rb / ra * tan(rad_lat_B))
        xx = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(rad_lng_A - rad_lng_B))
        c1 = (sin(xx) - xx) * (sin(pA) + sin(pB)) ** 2 / cos(xx / 2) ** 2
        c2 = (sin(xx) + xx) * (sin(pA) - sin(pB)) ** 2 / sin(xx / 2) ** 2
        dr = flatten / 8 * (c1 - c2)
        distance = ra * (xx + dr)
        return distance
    except:
        return 0

class AMap(object):
    def __init__(self, key):
        self._key = key

    def __request_of_get(self, url):
        for _ in range(5):
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    return json.loads(r.text)
            except:
                pass

        raise Exception('Reuqest %s failure' % (url,))

    def distance_between_position(self, from_longitude, from_latitude, to_longitude, to_latitude):
        """ 两点之间的距离 """

        url = 'http://restapi.amap.com/v3/distance?key={key}&origins={origin}&destination={destination}&type=1'
        result = self.__request_of_get(url.format(key=self._key,
                                                  origin='{from_longitude},{from_latitude}'.format(
                                                      from_longitude=from_longitude, from_latitude=from_latitude),
                                                  destination='{to_longitude},{to_latitude}'.format(
                                                      to_longitude=to_longitude, to_latitude=to_latitude)))

        return int(result['results'][0]['distance']) / 1000


def distance(from_longitude, from_latitude, to_longitude, to_latitude):
    amap = AMap('146c4228971a9f848eeb1b24c7dd005a')

    try:
        result = amap.distance_between_position(from_longitude, from_latitude, to_longitude, to_latitude)
    except:
        result = None

    if not result:
        result = distance_between_position(from_longitude, from_latitude, to_longitude, to_latitude)
        # 用户认为距离不准, 两点间距离 * 1.3
        result = result * 1.3

    return result
