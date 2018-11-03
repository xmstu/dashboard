# -*- coding: utf-8 -*-
import requests
import random
from lxml import etree

from server.configs import USER_AGENTS, QIANCHENG_CITY_CODE

SALARY = {
    '所有': '99',
    '2千以下': '01',
    '2-3千': '02',
    '3-4.5千': '03',
    '4.5-6千': '04',
    '6-8千': '05',
    '0.8-1万': '06',
    '1-1.5万': '07',
    '1.5-2万': '08',
    '2-3万': '09',
    '3-4万': '10',
    '4-5万': '11',
    '5万以上': '12',
}


def job_count_spider(search_name='python'):
    job_list = []
    job_list_dict = []
    for k, v in QIANCHENG_CITY_CODE.items():
        url = "https://search.51job.com/list/{},000000,0000,00,9,99,{},2,1.html".format(v, search_name)
        headers = {
            "User-Agent": random.choice(USER_AGENTS)
        }
        response = requests.get(url=url, headers=headers)
        data = response.content.decode('gbk')
        data.replace('0xa1', '')
        data = etree.HTML(data)
        count = data.xpath('//*[@id="resultList"]/div[2]/div[5]/text()')
        if not count:
            count = data.xpath('//*[@id="resultList"]/div[3]/div[5]/text()')
        count = str(count[1]).split('/')[1]
        count = int(count) * 50
        if k != "全国":
            job_list.append([k, count])
        job_list_dict.append({
            "region_name": k,
            "count": count
        })
    job_list_dict.sort(key=lambda k:k["count"], reverse=True)
    for index, detail_dict in enumerate(job_list_dict):
        detail_dict["percentage"] = "%.2f%%" % ((detail_dict["count"] / job_list_dict[0].get("count")) * 100)

    item = job_list_dict.pop(0)
    result = {
        "job_list": job_list,
        "job_list_dict": job_list_dict,
        "sum_count": item["count"]
    }
    return result


def job_news(search_name='python'):
    result = []
    url = 'https://mkt.51job.com/careerpost/default_res.php'
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
    }
    response = requests.get(url=url, headers=headers)

    data = response.content.decode('gbk')
    data = etree.HTML(data)
    node_list = data.xpath('/html/body/div[2]/div[2]/div[1]/div[2]/ul/li')

    for node in node_list:
        title = node.xpath('./a/text()')[0]
        href = node.xpath('./a/@href')[0]
        if 'http' not in href: href = 'https:' + href

        result_dict = {
            'title': title,
            'url': href
        }

        result.append(result_dict)
    return result


def job_money(search_name='python', city='全国'):
    city_code = QIANCHENG_CITY_CODE.get(city)
    job_salary_list = []
    job_salary_list_dict = []
    for k, v in SALARY.items():
        url = "https://search.51job.com/list/{},000000,0000,00,9,{},{},2,1.html".format(city_code, v, search_name)
        print("=" * 50, url)
        headers = {
            "User-Agent": random.choice(USER_AGENTS)
        }
        response = requests.get(url=url, headers=headers)

        data = response.content.decode('gbk')
        data.replace('0xa1', '')

        data = etree.HTML(data)
        count = data.xpath('//*[@id="resultList"]/div[2]/div[5]/text()')

        if not count:
            count = data.xpath('//*[@id="resultList"]/div[3]/div[5]/text()')
        count = str(count[1]).split('/')[1]
        count = int(count) * 50
        if k != "所有":
            job_salary_list.append([k, count])
        job_salary_list_dict.append({
            "row_name": k,
            "count": count
        })

    job_salary_list_dict.sort(key=lambda k: k["count"], reverse=True)
    for index, detail_dict in enumerate(job_salary_list_dict):
        detail_dict["percentage"] = "%.2f%%" % ((detail_dict["count"] / job_salary_list_dict[0].get("count")) * 100)

    item = job_salary_list_dict.pop(0)
    result = {
        "job_salary_list": job_salary_list,
        "job_salary_list_dict": job_salary_list_dict,
        "sum_count": item["count"]
    }
    return result


if __name__ == '__main__':
    search_name = "java"
    # print(job_count_spider(search_name))

    # print(job_news(search_name))

    print(job_money(search_name))
