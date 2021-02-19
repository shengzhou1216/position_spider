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

cookie = 'JSESSIONID=ABAAAECAAEBABII236533B72AD04387C58BBAEF92E48242; WEBTJ-ID=20210217134011-177ae80c802768-0b9786c38f28ee-4353760-1327104-177ae80c803836; RECOMMEND_TIP=true; index_location_city=%E5%85%A8%E5%9B%BD; sajssdk_2015_cross_new_user=1; sensorsdata2015session=%7B%7D; user_trace_token=20210217134024-93d7808b-ed6c-423c-91a6-3cec94d15e25; __lg_stoken__=59ac34ae6495c7995a689a9594aba0e1c3a8fc28ae5fd8b1cfa652e416b4c6017a05db450e4a62a6fda84cf0558ba4c7c31f1aeb8e809ddad9ae6148434a87cf688bbe5268c9; X_MIDDLE_TOKEN=8140b4a55171a02ac6df637b78a5e073; _ga=GA1.2.1994363303.1613540446; _gid=GA1.2.846640884.1613540446; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1613194655,1613540446; LGUID=20210217134052-98a3f5ba-a88b-4224-b3f0-44f302723294; TG-TRACK-CODE=search_code; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22177ae80fbe562f-053cfdc37d7cad-4353760-1327104-177ae80fbe6557%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2283.0.4103.116%22%7D%2C%22%24device_id%22%3A%22177ae80fbe562f-053cfdc37d7cad-4353760-1327104-177ae80fbe6557%22%7D; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1613545674; LGRID=20210217154341-63de2e9c-45d6-4143-9858-16b293f64196; X_HTTP_TOKEN=d1ad9a02ec4599c997605531616a97fc359620de80; SEARCH_ID=fa69bb704b3048d4a77c641af2a1ecce'
detail_cookie = 'SESSIONID=ABAAAECAAEBABIIC9C5A9035A7ECD679762399A58FE53FF; WEBTJ-ID=02192021%2C105533-177b836c77c9b5-01282c63719253-1e2e1b0b-1648656-177b836c77d1278; RECOMMEND_TIP=true; index_location_city=%E5%85%A8%E5%9B%BD; sajssdk_2015_cross_new_user=1; sensorsdata2015session=%7B%7D; _ga=GA1.2.1138532040.1613703338; _gid=GA1.2.1361933110.1613703338; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1613703339; user_trace_token=20210219105539-1935529d-b94d-498e-95c5-bcfc7137596f; LGSID=20210219105539-5532dfcb-ea6b-48b8-aa9c-842bf4d5ca75; LGUID=20210219105539-145370ca-0fa4-4478-af62-ab1687935f5a; __lg_stoken__=64f0ec0b3d36153bd482389b49cdd0ada7b0012a22b664fa9e30d2655005dcf803cf5462b480f88ce32e2c3a62a9f75f2ee7e8cf44cc8d62bf33400d0cea2df2ad7267f48ae2; X_MIDDLE_TOKEN=158eec6a338fdef4dc11990b47ed3ca6; SEARCH_ID=72b6b75a58f049b1b1c8578cdcf08c98; TG-TRACK-CODE=search_code; X_HTTP_TOKEN=eb64c8059176738a4834073161f2d27565626be941; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22177b836d83330a-0bccbaae45d1b7-1e2e1b0b-1648656-177b836d8341e8%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24os%22%3A%22UNIX%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2287.0.4280.88%22%7D%2C%22%24device_id%22%3A%22177b836d83330a-0bccbaae45d1b7-1e2e1b0b-1648656-177b836d8341e8%22%7D; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1613704387; LGRID=20210219111313-c99b4d9c-1521-4496-9140-147abaf902c1'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Cache-Control': 'no-cache',
    'Cookie': cookie,
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # referer是必须的
    'referer': 'https://www.lagou.com/jobs/list_%E5%89%8D%E7%AB%AF%E5%B7%A5%E7%A8%8B%E5%B8%88/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput='
}

detail_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Cache-Control': 'no-cache',
    'Cookie': detail_cookie,
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'referer': 'https://www.lagou.com/jobs/list_%E5%89%8D%E7%AB%AF%E5%B7%A5%E7%A8%8B%E5%B8%88/p-city_0?&cl=false&fromSearch=true&labelWords=&suginput='
}
proxies = {
    'http': 'socks5://127.0.0.1:1080'
}


def start():
    query('前端工程师')


def query(q):
    logging.info('获取【%s】职位信息', q)
    pn = 70
    data = {
        # 'first': 'true',
        'kd': q,
        'pn': pn,
    }
    while True:
        r = requests.post(baseUrl, data=data, headers=headers, verify=False)
        logging.info('r:%s', r)
        res = r.json()
        try:
            if not 'content' in res:
                logging.error('request error: %s', res['msg'])
                break
            total_count = res['content']['positionResult']['totalCount']
            page_size = res['content']['pageSize']
            page_no = res['content']['pageNo']
            result = res['content']['positionResult']['result']
            code = res['code']
            if code != 0:
                logging.error('get position error:%s,code:%d',
                              res['msg'], code)
                break
            logging.info('total_count: %d, page_size: %d,page_no: %d',
                         total_count, page_size, page_no)
            if not result or len(result) == 0:
                break
            data['pn'] += 1
        except Exception as e:
            logging.error('get position error:%s' % e.message)
        insert_lagou_positions(result)
        # with open('lagou.json','w+',encoding='utf8') as f:
        #     f.write(json.dumps(result))
        wait_times = random.randint(10, 30)
        logging.info('wait_times:%d then continue get position', wait_times)
        time.sleep(wait_times)


def do_process_positions():
    try:
        process_positions()
    except IndexError as e:
        logging.exception(e)
        wait_times = random.randint(60,120)
        logging.info('wait %d seconds,then continue process positions.',wait_times)
        time.sleep(wait_times)
        do_process_positions()
    except Exception as e:
        logging.exception(e)
    logging.info('done processing')

def process_positions():
    positions = lagou.find({'detail': {'$exists': False}})
    count = lagou.count_documents({'detail': {'$exists': False}})
    logging.info("positions count:%d",count)
    for p in positions:
        positionId = p['positionId']
        detail = get_detail_of_positon(positionId)
        p['detail'] = detail
        db.lagou.update_one({'positionId': positionId},{'$set': {'detail': detail}})
        time.sleep(random.randint(10, 60))


def get_detail_of_positon(positionId):
    position_url = 'https://www.lagou.com/jobs/%s.html' % positionId
    logging.info('positon_url:%s',position_url)
    r = requests.get(position_url, headers=detail_headers, verify=False,proxies=proxies)
    soup = BeautifulSoup(r.text,'lxml')
    return soup.select('.job-detail')[0].get_text()


if __name__ == '__main__':
    # start()
    do_process_positions()