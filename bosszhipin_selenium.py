# -*- coding: utf-8 -*-
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import os,logging,yaml
import logging.config
import requests

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

def get_positiono_requirements(jid,lid):
    logging.info('jid:%s,lid:%s',jid,lid)
    params = {
        'jid': jid,
        'lid': lid,
        'type': '3'
    }
    r = requests.get(url,params=params,headers=headers)
    logging.info(r.json())
    return r.json()['zpData']['html']  if r.status_code == requests.codes.ok and r.json()['code'] == 0 else None

def get_position():
    pagination = WebDriverWait(driver,wait_timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'.page'))
    )

    job_list_warpper = WebDriverWait(driver,wait_timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'.job-list'))
    )

    job_list_ul = driver.find_elements_by_css_selector('.job-list ul > li')

    for job_ele in job_list_ul:
        job_name_el = job_ele.find_element_by_css_selector('.job-title span a')
        job_name = job_name_el.text
        job_area = job_ele.find_element_by_css_selector('.job-title .job-area').text
        company = job_ele.find_element_by_css_selector('.info-company .company-text .name a').text
        company_url = 'https://www.zhipin.com' + job_ele.find_element_by_css_selector('.info-company .company-text .name a').get_attribute('href')
        job_limit_el = job_ele.find_element_by_css_selector('.job-limit')
        salary = job_limit_el.find_element_by_css_selector('span').text
        education = job_limit_el.find_element_by_css_selector('p').text
        tags_el = job_ele.find_elements_by_css_selector('.info-append .tags')
        tags = []
        for tag_el in tags_el:
            tags.append(tag_el.find_element_by_css_selector('.tag-item').text)

        desc = job_ele.find_element_by_css_selector('.info-append .info-desc').text

        primary_box = job_ele.find_element_by_css_selector('.primary-box')
        jid = primary_box.get_attribute('data-jid')
        lid = primary_box.get_attribute('data-lid')
        # requirements = get_positiono_requirements(jid,lid)
        job = {
            'name': job_name,
            'area': job_area,
            'company': company,
            'company_url': company_url,
            'salary': salary,
            'education': education,
            'tags': tags,
            'desc': desc,
            # 'requirements': requirements
        }

        logging.info('job: %s', job)

setup_logging()

firefox_binary = FirefoxBinary('D:\Software\Mozilla Firefox\\firefox.exe')
driver = webdriver.Firefox(firefox_binary=firefox_binary)
query = '前端工程师'
page = 1
url_format = 'https://www.zhipin.com/c100010000/?query=%s&page=%d'
wait_timeout = 10
driver.get(url_format  % (requests.utils.quote(query), page))

url = 'https://www.zhipin.com/wapi/zpgeek/view/job/card.json'
cookie = '__zp_stoken__=47a0bW05GATlMTBAQK1h8JG5tDjISagIbAEcrEDJvcClhABYrNF1gYgBtNxpkRmVrHkwJHBR0XwkIBnAkT0lqbElHDW8AeTJ5OX05P3dOVH1DdhV7bi0dSHk0d2QIIlQrGB0DJQd9DAB8fjhHPg%3D%3D; lastCity=100010000; __c=1613636987; __g=-; __a=76226856.1613636987..1613636987.1.1.1.1; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1613636987; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1613636987'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Cache-Control': 'max-age=0',
    'Cookie': cookie,
}

get_position()

next_page = driver.find_element_by_css_selector('.page .next')


if 'disable' not in next_page.get_attribute('class'):
    next_page.click()
    
logging.info(driver.current_url)

