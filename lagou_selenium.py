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

firefox_binary = FirefoxBinary('D:\Software\Mozilla Firefox\\firefox.exe')
driver = webdriver.Firefox(firefox_binary=firefox_binary)
query = '前端工程师'
page = 1
url_format = 'https://www.zhipin.com/c100010000/?query=%s&page=%d'
driver.get(url_format  % (query, page))
wait_timeout = 10

pagination = WebDriverWait(driver,wait_timeout).until(
    EC.presence_of_element_located((By.CSS_SELECTOR,'.page'))
)

next_page = WebDriverWait(driver,wait_timeout).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR,'.page .next'))
)

job_list_warpper = WebDriverWait(driver,wait_timeout).until(
    EC.presence_of_element_located((By.CSS_SELECTOR,'.job-list'))
)

job_list_ul = driver.find_elements_by_css_selector('.job-list ul > li')

for job_ele in job_list_ul:
    job_name = job_ele.find_element_by_css_selector('.job-title span a').text
    job_area = job_ele.find_element_by_css_selector('.job-title .job-area').text
    company = job_ele.find_element_by_css_selector('.info-company .company-text .name a').text
    company_url = 'https://www.zhipin.com' + job_ele.find_element_by_css_selector('.info-company .company-text .name a').get_attribute('href')
    driver.execute_script('document.querySelector(".job-list ul > li .info-detail").style.display="block"')
    position_detail_el =  WebDriverWait(driver,wait_timeout).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,'.job-list ul > li .info-detail .detail-bottom .detail-bottom-text'))
    )
    position_detail = position_detail_el.text
    tags_el = job_ele.find_element_by_css_selector('.info-append .tags')
    tags = []
    for tag_el in tags_el:
        tags.append(tag_el.find_element_by_css_selector('.tag-item').text)
    desc = job_ele.find_element_by_css_selector('.info-append .info-desc').text

    job = {
        'name': job_name,
        'area': job_area,
        'company': company,
        'company_url': company_url,
        'detail': position_detail,
        'tags': tags,
        'desc': desc
    }

    logging.info('job: %s', job)


driver.close()