# -*- coding: utf-8 -*-
import random
import time
import uuid
from threading import Thread, Lock

import redis
import requests
from lxml import etree

from server.configs import *

redis_conn = redis.StrictRedis(host=REDIS_SETTINGS['host'], db=REDIS_SETTINGS['db'], password=REDIS_SETTINGS['password'])

global_dict = {}

mutex_lock = Lock()


def gen_global_dict():
    global global_dict
    for word in WORDS:
        global_dict[word] = 0


gen_global_dict()


def job_list_spider(search_name='python', city='全国'):
    city_code = QIANCHENG_CITY_CODE[city]
    page_index = 1
    while True:
        url = "https://search.51job.com/list/{},000000,0000,00,9,99,{},2,{}.html".format(city_code, search_name, page_index)

        headers = {
            "User-Agent": random.choice(USER_AGENTS)
        }
        response = requests.get(url=url, headers=headers)

        data = response.content.decode('gbk')
        data.replace('0xa1', '')

        data = etree.HTML(data)

        job_node_list = data.xpath('//*[@id="resultList"]/div/p/span/a/@href')

        if not job_node_list:
            break

        for i, node in enumerate(job_node_list):
            put_detail_url(search_name=search_name, url=node, city=city, page_index=str(page_index) + '_' + str(i + 1))
        page_index += 1

        t = Thread(target=job_detail, args=(search_name, page_index, len(job_node_list)))
        t.start()


def put_detail_url(search_name='python', url='', city='全国', page_index="0"):
    put_dict = {
        "url": url,
        "page": page_index,
        "city": city,
        "uu": str(uuid.uuid4())
    }

    redis_conn.hset('{}'.format(search_name), page_index, put_dict)


def job_detail(search_name='python', page=1, page_len=50):

    time.sleep(2)
    for i in range(page_len):
        result = redis_conn.hget(search_name, str(page) + '_' + str(i + 1))
        # print(result)
        data = result.decode()
        result = eval(data)
        headers = {
            "User-Agent": random.choice(USER_AGENTS)
        }
        response = requests.get(url=result.get('url'), headers=headers)
        data = response.content.decode('gbk')
        data = data.replace('0xa1', '')
        data = data.replace('0xa0', '')

        data = etree.HTML(data)

        title = data.xpath('//h1/text()')

        if not title:
            continue
        title = title[0].strip()
        content = data.xpath('//div[@class="tCompany_main"]/div[1]')
        msg = content[0]
        h2 = msg.xpath('./h2/span/text()')[0]

        p = msg.xpath('./div/p/text()')
        if not p:
            p = msg.xpath('./div/text()')

            if not p[2].strip():
                p = msg.xpath('./div/p/span/text()')

        detail = ''.join(p)
        global global_dict, mutex_lock
        for word in WORDS:
            if word in detail:
                mutex_lock.acquire()
                global_dict[word] += 1
                # global_num += 1
                mutex_lock.release()

        print(title, h2, p, )


def get_job_detail_result(search_name, city):
    ret = redis_conn.hmget('{search_name}_{city}_result'.format(search_name=search_name, city=city), WORDS)
    if all(ret):
        ret = [int(i) for i in ret]
        result_dict = dict(zip(WORDS, ret))
    else:
        job_list_spider(search_name=search_name, city='深圳')
        result_dict = global_dict
        redis_conn.hmset('{search_name}_{city}_result'.format(search_name=search_name, city=city), result_dict)

    job_detail_list = []
    job_detail_list_dict = []
    for key, value in result_dict.items():
        job_detail_list.append([key, value])
        job_detail_list_dict.append({
            "direction": key,
            "count": value
        })

    return {
        "job_detail_list": job_detail_list,
        "job_detail_list_dict": job_detail_list_dict,
        "count": sum(result_dict.values()),
    }


if __name__ == '__main__':
    ret = redis_conn.hmget("golang_result", WORDS)
    print(ret)
    search_name = 'golang'
    city = "深圳"
    job_list_spider(search_name=search_name, city=city)
    redis_conn.hmset('{search_name}_{city}_result'.format(search_name=search_name, city=city), global_dict)
