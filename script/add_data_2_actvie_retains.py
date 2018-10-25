# -*- coding: utf-8 -*-


import time

from script.db import MySQLdb


if __name__ == '__main__':
    # 测试数据库
    reader = writer = MySQLdb({
        "maxConnections": 3,
        "port": 3306,
        "host": "huitouche2.mysql.rds.aliyuncs.com",
        "minFreeConnections": 1,
        "database": "sshuitouche",
        "password": "htctita337",
        "user": "sshtc_user",
        "charset": "utf8mb4",
        "keepConnectionAlive": True
    })



