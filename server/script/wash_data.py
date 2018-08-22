import time

import pymysql
from twisted.enterprise import adbapi
from twisted.internet import reactor


def handle(result_data):
    # 处理from_channel
    ret = []
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
                    ret.append({'from_channel': i['from_channel'], 'id': i['id']})
                else:
                    i['from_channel'] = download_channel
                    ret.append({'from_channel': i['from_channel'], 'id': i['id']})
        else:
            if from_channel:
                if from_channel == 'miniprogram':
                    pass
                elif from_channel == 'qudao=tuijian':
                    i['from_channel'] = '推荐注册'
                    ret.append({'from_channel': i['from_channel'], 'id': i['id']})
                elif from_channel not in ('qudao=tuijian', 'miniprogram'):
                    pass
                else:
                    i['from_channel'] = ''
                    ret.append({'from_channel': i['from_channel'], 'id': i['id']})
    del result_data
    return ret


def update_from_channel(cursor, sql):
    """更新数据"""
    try:
        rowcount = cursor.execute(sql)
        print('received rowcount:', rowcount)
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
        sshuitouche_db.runInteraction(select_shu_user, command)


def select_shu_user(cursor, sql):
    """查询"""
    cursor.execute(sql)
    result_data = handle(cursor.fetchall())
    for i in result_data:
        # 提交
        print('start')
        command = """UPDATE shu_user_profiles SET from_channel='{0}' WHERE id ={1}""".format(i['from_channel'], i['id'])
        sshuitouche_db.runInteraction(update_from_channel, command)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    print('finish')


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
