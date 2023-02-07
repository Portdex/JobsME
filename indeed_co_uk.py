import csv
import json
from dateutil import parser
import requests
from datetime import date as today_date
from playwright.sync_api import sync_playwright, ElementHandle
import os
import pymysql
from functions import connection_db
from playwright_stealth import stealth_sync
import time
host,user,password,database = connection_db()
connection = pymysql.connect(host=host, user=user, password=password, database=database)
cur = connection.cursor()
def get_category_id(category_name):
    cur = connection.cursor()
    cur.execute(f"SELECT id FROM categories where cat_name = '{category_name}'")
    re = cur.fetchall()
    if(len(re) > 0):
        id = re[0][0]
    else:
        cur.execute("INSERT INTO `categories`(`cat_name`) VALUES (%s)",(category_name))
        connection.commit()
        id = cur.lastrowid
    return id

def job_type_id(job_type):
    cur = connection.cursor()
    cur.execute(f"SELECT id FROM types where job_type = '{job_type}'")
    re = cur.fetchall()
    if(len(re) > 0):
        id = re[0][0]
    else:
        cur.execute("INSERT INTO `types`(`job_type`) VALUES (%s)",(job_type))
        connection.commit()
        id = cur.lastrowid
    return id

os.environ["BROWSER_PATH"] = "~/.cache/ms-playwright"
all_cat_jobs = ['Doctor','Security','Nurses','Health Care Worker','Social Worker']
Location = "London"
with sync_playwright() as p:
    browser = p.firefox.launch()
    page = browser.new_page()
    stealth_sync(page)
    for cat_jobs in all_cat_jobs:
        page.goto('https://uk.indeed.com/', timeout=50000)
        if page.locator('xpath=//*[@id="text-input-what"]'):
            what = page.locator('xpath=//*[@id="text-input-what"]')
            what.fill("")
            what.type(cat_jobs)
            where = page.locator('xpath=//*[@id="text-input-where"]')
            where.fill("")
            where.type(Location)
            page.locator('xpath=//form[@id="jobsearch"]/button').click()
            i = 1
            while i <= 10:
                time.sleep(4)
                page.wait_for_load_state()
                try:
                    # google model close button 
                    page.locator('button.icl-CloseButton.icl-Card-close').click()
                except:
                    pass
                try:
                    # newsletter model close button 
                    page.locator('button.icl-CloseButton.icl-Modal-close').click()
                except:
                    pass
              
                all_list_li = page.locator('//*[@id="mosaic-provider-jobcards"]/ul/li').all()
                for single_list in all_list_li:
                    try:
                        single_list.click()
                        apply_link = single_list.locator('h2.jobTitle a').get_attribute("href")
                        apply_link = f"https://uk.indeed.com{apply_link}"
                    except Exception as e:
                        print(e)
                        continue
                    time.sleep(3)
                    try:
                        job_title = page.locator("h2.jobsearch-JobInfoHeader-title").inner_text().replace("- job post","").strip()
                    except:
                        job_title = ""
                    try:
                        company_name = page.locator("div.css-czdse3.eu4oa1w0 a").inner_text().strip()
                    except:
                        company_name = ""
                    try:
                        salary = page.locator("span.css-2iqe2o.eu4oa1w0").all()[0].inner_text().strip()
                    except:
                        salary = ""
                    try: 
                        job_types = []
                        all_job_types = page.locator("div.css-1hplm3f.eu4oa1w0 div").all()
                        for index,types in enumerate(all_job_types):
                            if index == 0:
                                continue
                            job_types.append(types.inner_text().strip())
                    except:
                        job_types = ""
                    try:
                        descripition = page.locator("div.jobsearch-jobDescriptionText p").all()[0].inner_text().strip()
                    except:
                        descripition = ""
                    try:
                        location = page.locator("div.jobsearch-JobInfoHeader-subtitle div").all()[1].inner_text().strip()
                    except:
                        location = ""   
                    if apply_link != "":
                        try:
                            data = cur.execute(f"SELECT * FROM jobs WHERE apply_link = '{apply_link}'")
                            if not data > 0:
                                category_id = get_category_id(cat_jobs)
                                cur.execute(f'INSERT INTO `jobs`(`website_id`, `category_id`, `title`, `salary`, `description`, `apply_link`,`location`) VALUES ("2","{category_id}","{job_title}","{salary}","{descripition}","{apply_link}","{Location}")')
                                job_id = connection.insert_id()
                                connection.commit()
                                if job_types != "":
                                    for job_type in job_types:
                                        job_type_id_get = job_type_id(job_type)
                                        cur.execute(f"INSERT INTO `job_types`(`job_id`, `job_type_id`) VALUES ('{job_id}','{job_type_id_get}')")
                                connection.commit()
                        except Exception as ex:
                            print(ex)
                            pass
                try:
                    try:
                        page.locator('a.css-13p07ha.e8ju0x50').all()[1].click()
                    except:
                        page.locator('a.css-13p07ha.e8ju0x50').all()[0].click()
                except Exception as ex:
                    print(ex)
                    pass
                i+=1
connection.close() 