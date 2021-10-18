# -*- coding: utf-8 -*-
from os.path import join
import requests
from bs4 import BeautifulSoup
import os
import logging
import logging.config
import urllib3
import yaml
import json
from db import insert_lagou_positions, lagou
import db
import time
import random
import requests
from bs4 import BeautifulSoup


def setup_logging(default_path="logging.yaml", default_level=logging.INFO, env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p', filename='example.log', level=default_level)


setup_logging()


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
baseUrl = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'

cookie = 'user_trace_token=20210219115644-bb71ccd2-85c4-499d-8e4e-6f774d97da1a; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22177b86ecfec426-00f581605e814d8-7d21675c-1648656-177b86ecfed950%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24os%22%3A%22UNIX%22%2C%22%24browser%22%3A%22Firefox%22%2C%22%24browser_version%22%3A%2293.0%22%7D%2C%22%24device_id%22%3A%22177b86ecfec426-00f581605e814d8-7d21675c-1648656-177b86ecfed950%22%7D; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1634177353,1634526352; _ga=GA1.2.1909959156.1613707006; LGUID=20210219115645-c321d6a2-7fd8-4dbe-a450-6a291bac893c; RECOMMEND_TIP=true; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAABAGABFA3D453B74218F42A98297F8C6AFD9793F; WEBTJ-ID=10182021%2C110552-17c915cd2e43b-0e6ba7b275427a8-7b26675d-2359296-17c915cd2e56d7; X_HTTP_TOKEN=aaded26f5dbc377a1876254361770349f116989208; LGSID=20211018110552-edf78c32-9244-4fbc-a1e6-d651e305b1ea; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGRID=20211018111301-913f73e3-2973-48d2-9fb8-48851919a26c; _gat=1; sensorsdata2015session=%7B%7D; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1634526782; privacyPolicyPopup=false; _gid=GA1.2.1737420682.1634526353; TG-TRACK-CODE=index_checkmore; __lg_stoken__=a2128bb8855b123630405cd5f6bd545f86755fc3c442b8a0c19499de154148081d4ae13915ffded8f096cde0bf3a7e47b9a5699b5bec4af36b3c8d36b77fba380baa79998b5d; X_MIDDLE_TOKEN=8b889f2ba7185560de9aea9504864585; SEARCH_ID=3cb761c62afc4a9eb85aa1e7883ce8d7'

detail_cookie = 'JSESSIONID=ABAAAECAAEBABIIC9C5A9035A7ECD679762399A58FE53FF; WEBTJ-ID=02192021%2C105533-177b836c77c9b5-01282c63719253-1e2e1b0b-1648656-177b836c77d1278; RECOMMEND_TIP=true; index_location_city=%E5%85%A8%E5%9B%BD; sensorsdata2015session=%7B%7D; _ga=GA1.2.1138532040.1613703338; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1613703339; user_trace_token=20210219105539-1935529d-b94d-498e-95c5-bcfc7137596f; LGUID=20210219105539-145370ca-0fa4-4478-af62-ab1687935f5a; __lg_stoken__=64f0ec0b3d36153bd482389b49cdd0ada7b0012a22b664fa9e30d2655005dcf803cf5462b480f88ce32e2c3a62a9f75f2ee7e8cf44cc8d62bf33400d0cea2df2ad7267f48ae2; X_MIDDLE_TOKEN=158eec6a338fdef4dc11990b47ed3ca6; TG-TRACK-CODE=search_code; _gid=GA1.2.1562694723.1613793617; PRE_UTM=; PRE_HOST=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F7977723.html; LGSID=20210220120019-523d6559-e25b-4c09-83d4-68dbbfbef1ff; PRE_SITE=; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22177b836d83330a-0bccbaae45d1b7-1e2e1b0b-1648656-177b836d8341e8%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24os%22%3A%22UNIX%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2287.0.4280.88%22%7D%2C%22%24device_id%22%3A%22177b836d83330a-0bccbaae45d1b7-1e2e1b0b-1648656-177b836d8341e8%22%7D; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1613793791; LGRID=20210220120313-29080882-f07b-409e-a8a0-61bb809e8310; X_HTTP_TOKEN=eb64c8059176738a8183973161f2d27565626be941'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Cache-Control': 'no-cache',
    'Cookie': cookie,
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # referer是必须的
    'referer': 'https://www.lagou.com/jobs/list_%E5%89%8D%E7%AB%AF%E5%B7%A5%E7%A8%8B%E5%B8%88/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput=',
}

detail_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Cache-Control': 'no-cache',
    'Cookie': detail_cookie,
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'referer': 'https://www.lagou.com/utrack/trackMid.html?f=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F7977723.html&t=1613793639&_ti=3'
}

# 免费代理: https://ip.jiangxianli.com/?page=1, https://www.kuaidaili.com/free/ , http://www.xiladaili.com/, https://zhuanlan.zhihu.com/p/334357097

proxies = {
    # 'http': 'http://127.0.0.1:1080',
    'https': 'http://178.134.208.126:50824',
    'https': 'http://118.117.188.171:3256',
    'https': 'http://104.254.238.122:20171',
    'https': 'http://185.179.30.130:8080',
}


def start():
    query('Golang')


def query(q):
    logging.info('获取【%s】职位信息', q)
    pn = 77
    data = {
        # 'first': 'true',
        'kd': q,
        'pn': pn,
    }
    while True:
        r = requests.post(baseUrl, data=data, headers=headers, proxies=proxies,
                          verify=False,)
        logging.info('r:%s,%s', r.status_code, r.reason)
        res = r.json()
        try:
            if not 'content' in res:
                logging.error('there is no content in res: %s', res)
                state = res['state']
                status = res['status']
                if status == False or state == 2043 or state == 2045:
                    # 操作频繁
                    logging.info(
                        'wait_times:%d then continue get position', 120)
                    time.sleep(120)
                    continue
                break
            total_count = res['content']['positionResult']['totalCount']
            page_size = res['content']['pageSize']
            page_no = res['content']['pageNo']
            result = res['content']['positionResult']['result']
            code = res['code']
            if code != 0:
                logging.error('get position error:%s,code:%d',
                              res['msg'], code)
                # break
            logging.info('total_count: %d, page_size: %d,page_no: %d',
                         total_count, page_size, page_no)
            if not result or len(result) == 0:
                break
            data['pn'] += 1
        except Exception as e:
            logging.error('get position error:%s' % e)
        insert_lagou_positions(result)
        # with open('lagou.json','w+',encoding='utf8') as f:
        #     f.write(json.dumps(result))
        # 处理请求频率限制
        wait_times = random.randint(20, 60)
        logging.info('wait_times:%d then continue get position', wait_times)
        time.sleep(wait_times)


def do_process_positions():
    try:
        process_positions()
    except IndexError as e:
        logging.exception(e)
        wait_times = random.randint(60, 120)
        logging.info(
            'wait %d seconds,then continue process positions.', wait_times)
        time.sleep(wait_times)
        do_process_positions()
    except Exception as e:
        logging.exception(e)
    logging.info('done processing')


def process_positions():
    positions = lagou.find({'detail': {'$exists': False}})
    count = lagou.count_documents({'detail': {'$exists': False}})
    logging.info("positions count:%d", count)
    for p in positions:
        positionId = p['positionId']
        detail = get_detail_of_positon(positionId)
        p['detail'] = detail
        db.lagou.update_one({'positionId': positionId}, {
                            '$set': {'detail': detail}})
        time.sleep(random.randint(10, 60))


def get_detail_of_positon(positionId):
    position_url = 'https://www.lagou.com/jobs/%s.html' % positionId
    logging.info('positon_url:%s', position_url)
    r = requests.get(position_url, headers=detail_headers, verify=False)
    print(r.text)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup.select('.job-detail')[0].get_text()


def store_to_file():
    details = db.lagou.find(
        {'positionDetail': {'$exists': True}, '$or': {'positionName': {'$regex': 'Go'}, 'thirdType': {'$regex': 'Go'}}})
    with open('lagou.txt', 'w', encoding='utf8') as f:
        for d in details:
            f.write(d['positionDetail'])


if __name__ == '__main__':
    start()
    # do_process_positions()
    # store_to_file()
