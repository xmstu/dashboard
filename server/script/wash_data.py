import time

import pymysql
from twisted.enterprise import adbapi
from twisted.internet import reactor

# 全局对象
select_data = []


def handle(result_data):
    # 处理from_channel
    for i in result_data:
        download_channel = i.get('download_channel')
        from_channel = i.get('from_channel')
        # 下载渠道不为空
        if download_channel:
            if from_channel:
                if from_channel == 'miniprogram':
                    pass
                elif from_channel == 'qudao=tuijian':
                    i['from_channel'] = '推荐注册'
                else:
                    i['from_channel'] = download_channel
        else:
            if from_channel:
                if from_channel == 'miniprogram':
                    pass
                elif from_channel == 'qudao=tuijian':
                    i['from_channel'] = '推荐注册'
                elif from_channel not in ('qudao=tuijian', 'miniprogram'):
                    pass
                else:
                    i['from_channel'] = ''

    return result_data


def update_from_channel(cursor):
    """更新数据"""
    try:
        command = """UPDATE shu_user_profiles SET from_channel=%s WHERE id =%s"""
        rowcount = cursor.executemany(command, select_data)
        select_data.clear()
        print('finish')
        print(rowcount)
    except Exception as e:
        print(e)


def main():
    """更新from_channel字段"""
    sshuitouche_db.runInteraction(select_shu_user_profiles)


def select_shu_user_profiles(cursor):

    cursor.execute("""SELECT count(1) all_count FROM `shu_user_profiles` WHERE is_deleted = 0""")
    all_count = cursor.fetchone()['all_count']
    # 分片查询
    for step in range(0, all_count, 10000):
        command = """
            SELECT
                id,
                from_channel,
                download_channel 
            FROM
                `shu_user_profiles` 
            WHERE
                is_deleted = 0
            LIMIT 10000 OFFSET %s
            """ % step
        sshuitouche_db.runInteraction(select_shu_user, command, all_count)


def select_shu_user(cursor, sql, all_count):
    """查询"""
    cursor.execute(sql)
    result_data = handle(cursor.fetchall())
    for i in result_data:
        data = [i['from_channel'], i['id']]
        select_data.append(data)
        # 提交
        if len(select_data) == all_count:
            print('start')
            sshuitouche_db.runInteraction(update_from_channel)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), len(select_data), all_count)


if __name__ == '__main__':
    # 业务库数据库基本配置
    # db_settings = {
    #     'host': '101.37.176.18',
    #     'db': 'sshuitouche',
    #     'user': 'sshtcread',
    #     'password': 'wJI83&d3$Rop2c',
    #     'charset': 'utf8',
    #     'cursorclass': pymysql.cursors.DictCursor,
    #     'use_unicode': True
    # }
    # 测试数据库基本配置
    db_settings = {
        'host': '112.124.232.175',
        'db': 'sshuitouche',
        'user': 'sshtc_user',
        'password': 'htctita337',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor,
        'use_unicode': True
    }
    try:
        sshuitouche_db = adbapi.ConnectionPool(dbapiName='pymysql', **db_settings)
        main()
    except Exception as e:
        print(e)

    reactor.callLater(4, reactor.stop)
    reactor.run()
