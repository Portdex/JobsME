import re
import time
import requests
from playwright.sync_api import sync_playwright, ElementHandle
import os
import pymysql
from functions import connection_db
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

def agency_id(agency):
    cur = connection.cursor()
    cur.execute(f"SELECT id FROM agency where name = '{agency}'")
    re = cur.fetchall()
    if(len(re) > 0):
        id = re[0][0]
    else:
        cur.execute("INSERT INTO `agency`(`name`) VALUES (%s)",(agency))
        connection.commit()
        id = cur.lastrowid
    return id

Location = "London"
category_send = "Doctor"
os.environ["BROWSER_PATH"] = "~/.cache/ms-playwright"
with sync_playwright() as p:
    browser = p.firefox.launch(
        )
    page = browser.new_page()
    page.goto('https://www.seek.com.au/', timeout=50000)
    page.locator('input#keywords-input').type(category_send)
    page.locator('input#SearchBar__Where').type(Location)
    time.sleep(3)
    page.locator('div.yvsb870._14wvm1j2 button').click()
    current_url = page.url
    total_pages = page.locator('span#SearchSummary h1.yvsb870').inner_text().replace("jobs","").replace(",","").strip()
    for current_page in range(1,int(total_pages)):
        all_vacancy_detail_links = []
        if current_page != 1:
            page.goto(f"{current_url}?page={current_page}")
        all_jobs = page.locator('article').all()
        for job in all_jobs:
            job_link = job.locator('h3 a').get_attribute("href")
            all_vacancy_detail_links.append(f"https://www.seek.com.au{job_link}")
        for detail_link in all_vacancy_detail_links:
            page.goto(detail_link)
            try:
                job_title = page.locator('h1.yvsb870._14uh9944u._1cshjhy0._1cshjhyl._1d0g9qk4._1cshjhyp._1cshjhy21').inner_text()
            except:
                job_title = ""
            try:
                apply_link = page.locator('a[data-automation=job-detail-apply]').all()[0].get_attribute("href")
                apply_link = f"https://www.seek.com.au{apply_link}"
            except:
                appply_link = ""
            try:
                agency_name = page.locator('span[data-automation=advertiser-name]').inner_text().strip()
                agency = agency_id(agency_name)
            except:
                agency = ""
            try:
                company_name = page.locator('span[data-automation=advertiser-name]').inner_text().strip()
            except:
                company_name = ""
            try:
                job_type = page.locator('span[data-automation=job-detail-work-type]').inner_text().strip()
            except:
                job_type = ""
            try:
                description = page.locator('div[data-automation=jobAdDetails]').inner_text().strip()
            except:
                description = ""
            try:
                category = page.locator('a[data-automation=jobClassification]').inner_text().strip()
            except:
                category = ""
            if apply_link != "":
                try:
                    data = cur.execute(f"SELECT * FROM jobs WHERE apply_link = '{apply_link}'")
                    if not data > 0:
                        if category != "":
                            category_id = get_category_id(category)
                        else:
                            category_id = get_category_id(category_send)
                        cur.execute(f'INSERT INTO `jobs`(`website_id`, `category_id`, `title`, `description`, `apply_link`,`location`,`agency_id`) VALUES ("3","{category_id}","{job_title}","{description}","{apply_link}","{Location}","{agency}")')
                        job_id = connection.insert_id()
                        connection.commit()
                        if job_type != "":
                            job_type_id_get = job_type_id(job_type)
                            cur.execute(f"INSERT INTO `job_types`(`job_id`, `job_type_id`) VALUES ('{job_id}','{job_type_id_get}')")
                        connection.commit()
                except Exception as ex:
                    print(ex)
                    pass

            
            
            