import time

from script.db import MySQLdb


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
                elif from_channel in ('上门安装',
                                      '上门推荐',
                                      '亲友介绍',
                                      '今日头条',
                                      '传单',
                                      '传单海报',
                                      '其他',
                                      '司机介绍',
                                      '合作伙伴',
                                      '应用市场',
                                      '微信分享',
                                      '微信朋友圈',
                                      '朋友',
                                      '横幅',
                                      '油站广告',
                                      '电话推广',
                                      '短信',
                                      '短信电话',
                                      '网络搜索',
                                      '车身广告',):
                    i['from_channel'] = ''
                    ret.append({'from_channel': i['from_channel'], 'id': i['id']})
    del result_data
    return ret


if __name__ == '__main__':

    # 测试数据库
    # reader = MySQLdb({
    #     "maxConnections": 3,
    #     "port": 3306,
    #     "host": "huitouche2.mysql.rds.aliyuncs.com",
    #     "minFreeConnections": 1,
    #     "database": "sshuitouche",
    #     "password": "htctita337",
    #     "user": "sshtc_user",
    #     "charset": "utf8mb4",
    #     "keepConnectionAlive": True
    # })

    # 线上业务库
    reader = MySQLdb({
        "maxConnections": 3,
        "port": 3306,
        "host": "101.37.176.18",
        "minFreeConnections": 1,
        "database": "sshuitouche",
        "password": "wJI83&d3$Rop2c",
        "user": "sshtcread",
        "charset": "utf8mb4",
        "keepConnectionAlive": True
    })

    try:
        with reader.begin() as db:
            all_count = \
            db.conn.query_one("""SELECT count(1) all_count FROM `shu_user_profiles` WHERE is_deleted = 0""")[
                'all_count']
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
                result_data = handle(db.conn.query(command))
                print('start')
                # 提交
                cmd = """UPDATE shu_user_profiles SET from_channel=:from_channel WHERE id =:id"""
                rowcount = db.conn.update(cmd, result_data)
                print('finished rowcount:', rowcount)
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), len(result_data))
                print('finish')
                print('\t')

    except Exception as e:
        print(e)
