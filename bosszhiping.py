# -*- coding: utf-8 -*-
from os.path import join
from bson.py3compat import b
import requests
from bs4 import BeautifulSoup
import os
import logging
import logging.config
import urllib3
import yaml
import json
import db
import time,random

def setup_logging(default_path= "logging.yaml",default_level=logging.INFO,env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key,None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path,'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename='example.log',level=default_level)

setup_logging()



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
baseUrl = 'https://www.zhipin.com/c100010000'
# baseUrl = 'https://www.zhipin.com/c100010000/?query=%s&page=%d'

cookie = '__zp_stoken__=d820bWGJgcwMKLxEFC3lBJFsrFhB%2FKToaaxwjHysEamQcbFoGJR9QDmg7TnNxPVZlJmR%2BHzNwLzV%2BBkFCDn8xUUd3QlMoVx9zE21rUSxwMj4FMWJ4VgsJIAEBbR0ZfQMMIDV0JiAONT8LAwkhfA%3D%3D'

cookie2 = 'lastCity=100010000; __g=-; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1613570547; __c=1613570547; __l=l=%2Fwww.zhipin.com%2Fc100010000%2F%3Fquery%3D%2525E5%252589%25258D%2525E7%2525AB%2525AF%2525E5%2525B7%2525A5%2525E7%2525A8%25258B%2525E5%2525B8%252588%26page%3D1&s=3&friend_source=0; __a=24397771.1613570547..1613570547.5.1.5.5; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1613635259; __zp_stoken__=47a0bWyB5WgRgQhRjZVh5X0FdaAcxQF91UEd3E3lqEWEpXQhXPgZLbxZSNx5jNnlKHkwJHBR0X35xe3AkSg9wGzBPeE8PCAkvIHZASmtXVH1DdhV7TzFtT300SHIFCQ8hGB0DJQd9DAB8fjhHPg%3D%3D'
#Fix: UnicodeEncodeError: 'latin-1' codec can't encode character '\u2026' in position 512: ordinal not in range(256)
referer = 'https://www.zhipin.com/web/common/security-check.html?seed=F4%2BLIK5lJcJde%2Fer8V5rkXS7dq6aSW8%2FP2VelXZU5Rg%3D&name=b9832fbe&ts=1613557821100&callbackUrl=%2Fc100010000%2F%3Fquery%3D%25E5%2589%258D%25E7%25AB%25AF%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588%26page%3D1&srcReferer=https%3A%2F%2Fwww.zhipin.com%2Fweb%2Fcommon%2Fsecurity-check.html%3Fseed%3DF4%252BLIK5lJcJde%252Fer8V5rked75bjUWZWuC%252F%252FSfKlAPaI%253D%26name%3Db9832fbe%26ts%3D1613557820883%26callbackUrl%3D%252Fc100010000%252F%253Fquery%253D%2…y-check.html%25253Fseed%25253DF4%2525252BLIK5lJcJde%2525252Fer8V5rked75bjUWZWuC%2525252F%2525252FSfKlAPaI%2525253D%252526name%25253Db9832fbe%252526ts%25253D1613557820381%252526callbackUrl%25253D%2525252Fc100010000%2525252F%2525253Fquery%2525253D%25252525E5%2525252589%252525258D%25252525E7%25252525AB%25252525AF%25252525E5%25252525B7%25252525A5%25252525E7%25252525A8%252525258B%25252525E5%25252525B8%2525252588%25252526page%2525253D1%252526srcReferer%25253Dhttps%2525253A%2525252F%2525252Fwww.zhipin.com%2525252F'.encode('utf8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Cookie': cookie,
    'Host': 'www.zhipin.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'TE': 'Trailers',
    'Upgrade-Insecure-Requests': '1',
    # referer是必须的
    # 'referer': referer
}

def start():
    query('前端工程师')

def query(q):
    logging.info('获取【%s】职位信息',q)
    pn = 1
    while True:
        params = {
            'page': pn,
            'query': requests.utils.quote(q)
        }
        # url = baseUrl % (params['query'], params['page'])
        r = requests.get(baseUrl,params=params,headers=headers,verify=False)
        logging.info('url:%s',r.url)
        logging.info(r.headers)

        headers['Cookie'] =  cookie2
        r = requests.get(r.url,headers=headers,verify=False)
        logging.info('url:%s',r.url)
        logging.info(r.headers)
        logging.info(r.text)

        if r.status_code != requests.codes.ok:
            continue
        results = []
        try:
            soup = BeautifulSoup(r.text,'lxml')
            job_list = soup.select('div.job-list ul > li')
            for job in job_list:
                name = job.select_one('.job-name a').text  
                area = job.select_one('.job-area').text
                company = job.select_one('.company-text .name a').text
                company_url = job.select_one('.company-text .name a')['href']
                industry = job.select_one('.company-text p > a').text
                tags_el = job.select_one('.info-append .tags .tag-item')
                tags = []
                for tag_el in tags_el:
                    tags.append(tag_el.text)
                desc = job.select_one('.info-desc').text
                result = {
                    'name': name,
                    'area': area,
                    'company': company,
                    'company_url': company_url,
                    'industry': industry,
                    'tags': tags,
                    'desc':desc,
                }
                results.append(result)
            pn += 1
        except Exception as e:
            logging.error('get position error:%s' % e.message)
        db.insert_bosszhipin_positions(results)

if __name__ == '__main__':
    start()