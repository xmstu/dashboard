# -*- coding: utf-8 -*-

import redis, time

from server import log

class ExtendRedis(object):
    def __init__(self, ip, port, db):
        self.ip = ip
        self.port = port
        self.db = db
        self.conn = redis.StrictRedis(host=self.ip, port=self.port, db=self.db)


    def read_one(self, key):
        data = self.conn.get(key)
        if not data:
            return
        data = eval(data.decode('utf8'))
        return data

    def read_georadius(self, key, longitude, latitude, radius, unit):
        try:
            data = self.conn.georadius(key, longitude, latitude, radius, unit)
            if not data:
                return
            return data
        except Exception as e:
            log.warn('read_georadius_failed: %s' % e, exc_info=True)
