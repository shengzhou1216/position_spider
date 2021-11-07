# -*- coding: utf-8 -*-
import string
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions 
import re
import json
import os
import logging
import logging.config
import time
import random
import yaml

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
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename='bosszhiping.log',level=default_level)

setup_logging()

# common wait timeout
wait_timeout = 10
# position results
results = []

# read exists data from
json_file = 'golang.json'
text_file = 'golang.txt'
if os.path.exists(json_file):
    with open(json_file, 'r',encoding='utf8') as f:
        results = json.load(f)

logging.info('original results:%d' ,len(results))

options = Options()
options.binary_location = r"D:\Software\Mozilla Firefox\firefox.exe"
# driver = webdriver.Firefox(executable_path="D:\Enviroments\selenium-driver\geckodriver.exe")
driver = webdriver.Firefox(options=options)

try:
    driver.get("https://www.zhipin.com/shanghai/")

    query = WebDriverWait(driver,wait_timeout).until(
        EC.presence_of_element_located((By.NAME,"query"))
    )
    query.send_keys('GoLang')
    query.send_keys(Keys.ENTER)

    # iterate per page
    # has next page
    while True:
        logging.info('url:%s',driver.current_url)
        # extract one page
        job_list = WebDriverWait(driver,wait_timeout).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div.job-list ul > li"))
        )

        jobs = []

        # filter exists job
        for job in job_list:
            href = job.find_element(By.CSS_SELECTOR,'.primary-box').get_attribute('href')
            matches = re.search(r"\/job_detail\/(\S*)\.html", href)
            if matches:
                job_id = matches.group(1)
                if job_id not in [x['id'] for x in results]:
                    jobs.append(job)

        logging.info('jobs count:%s',len(jobs))

        # original window 
        original_window = driver.current_window_handle

        job_id_regex = r"https:\/\/www\.zhipin\.com\/job_detail\/(\S*)\.html"

        for job in jobs:
            # sleep a while
            time.sleep(5)
            try:
                # click job item
                job.click()
                # switch to job detail tab
                # Wait for the new window or tab
                WebDriverWait(driver,wait_timeout).until(
                    EC.number_of_windows_to_be(2)
                )

                # Loop through until we find a new window handle
                for window_handle in driver.window_handles:
                    if window_handle != original_window:
                        driver.switch_to.window(window_handle)
                        break

                # processing job
                job_url = WebDriverWait(driver,wait_timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,'head link[rel="canonical"]'))
                )
                job_url = job_url.get_attribute('href')
                logging.info('job_url: %s',job_url)
                job_id = None
                matches = re.search(job_id_regex, job_url)
                if matches:
                    job_id = matches.group(1)
                    
                if job_id is not None and job_id not in [x['id'] for x in results]:
                    
                    time.sleep(3)

                    logging.info('job_id %s is not in results. trying to save it', job_id)
                        
                    job_desc = WebDriverWait(driver,wait_timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,'div.job-sec:nth-child(1) > div:nth-child(2)'))
                    )
                    job_name = WebDriverWait(driver,wait_timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,'.job-primary > div:nth-child(2) > div:nth-child(2) > h1:nth-child(1)'))
                    )
                    job_salary = WebDriverWait(driver,wait_timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,'.salary'))
                    )

                    job_tags = []
                    try:
                        job_tags = WebDriverWait(driver,wait_timeout).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR,'div.tag-container-new:nth-child(3) > div:nth-child(2) span'))
                        )
                        job_tags = [tag.text for tag in job_tags]
                    except exceptions.TimeoutException as e:
                        logging.exception('No tags found for this job.',e)
                            
                    company = WebDriverWait(driver,wait_timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,'.sider-company > div:nth-child(2) > a:nth-child(2)'))
                    )
                    company = company.text

                    results.append({
                            'name':job_name.text,
                            'salary':job_salary.text,
                            'desc':job_desc.text,
                            'href':job_url,
                            'tags': job_tags,
                            'id':job_id,
                            'company':company
                        })
                else:
                    logging.info('Job %s already exists.skip it.',job_id)
            except Exception as e:
                logging.exception(e)
            finally:
                # close the tab
                driver.close()
                # switch to original_window
                driver.switch_to.window(original_window)

            pages = WebDriverWait(driver,wait_timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'.page'))
            )

        try:
            next_btn = WebDriverWait(driver,wait_timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'.page .next'))
            )
            next_btn_class = next_btn.get_attribute('class')
            if next_btn_class.find('disabled') >= 0:
                logging.info('The next page btn is disabled.No more data.')
                break
            next_btn.click()
        except exceptions.TimeoutException as e:
            logging.exception('get next btn timeout:',e)
            break
        finally:
            with open(json_file,'+w', encoding='utf8') as f:
                json.dump(results,f,ensure_ascii=False,indent=4)
    # results count
    logging.info('results count:%s',len(results))

except Exception as e:
    logging.exception('Unkonw exception, quit browser!',e)
    # quit browser 
    driver.quit()