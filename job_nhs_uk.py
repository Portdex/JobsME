import re
import time
import requests
from playwright.sync_api import sync_playwright, ElementHandle
import os
import pymysql
from functions import connection_db
import dateparser
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
with sync_playwright() as p:
    browser = p.firefox.launch(
        )
    page = browser.new_page()
    page.goto('https://www.jobs.nhs.uk/xi/search_vacancy', timeout=50000)
    page.locator("button[name='searchBtn1']").click()
    total_pages =  page.locator("div.total").inner_text().split("of")[1].strip()
    for current_page in range(1,int(total_pages)):
        all_vacancy_detail_links = []
        if current_page != 1:
            page.goto(f"https://www.jobs.nhs.uk/xi/search_vacancy?action=page&page={current_page}")
        all_vaccncies = page.locator("div.vacancy").all()
        for vacancy in all_vaccncies:
            vacancy_data = {}        
            try:    
                vacancy_detail_link = vacancy.locator("h2 a").get_attribute("href")
            except:
                vacancy_detail_link = ""
            try:
                vacancy_title = vacancy.locator("h2 a").inner_text().strip()
            except:
                vacancy_title = ""
            try:
                vacancy_category = vacancy.locator("h3").inner_text().strip()
            except:
                vacancy_category = ""
            try:
                location = vacancy.locator("p.agency").inner_text().strip()
            except:
                location = ""
            try:
                description = vacancy.locator("p").all()[1].inner_text().strip()
            except:
                description = ""
            try:
                salary = vacancy.locator("div.vacancy-summary div.left dl").all()[0].inner_text().split(":")[1].strip()
            except:
                salary = ""
            try:
                posted_date = vacancy.locator("div.vacancy-summary div.left dl").all()[1].inner_text().split(":")[1].strip()
                posted_date = dateparser.parse(posted_date)
            except:
                posted_date = ""
            try:
                job_type = vacancy.locator("div.vacancy-summary div.left dl").all()[2].inner_text().split(":")[1].strip()
            except:
                job_type = ""
            try:
                closing_date = vacancy.locator("div.vacancy-summary div.right dl").all()[0].inner_text().split(":")[1].strip()
                closing_date = dateparser.parse(closing_date)
            except:
                closing_date = ""
            try:
                staff_group = vacancy.locator("div.vacancy-summary div.right dl").all()[1].inner_text().split(":")[1].strip()
            except:
                staff_group = ""
            try:
                job_ref = vacancy.locator("div.vacancy-summary div.right dl").all()[2].inner_text().split(":")[1].strip()
            except:
                job_ref = ""
            all_vacancy_detail_links.append({'vacancy_detail_link':vacancy_detail_link,'vacancy_title':vacancy_title,'vacancy_category':vacancy_category,'location':location,'description':description,'salary':salary,'posted_date':posted_date,'job_type':job_type,'closing_date':closing_date,'staff_group':staff_group,'job_ref':job_ref})
        for detail_link in all_vacancy_detail_links:
            detail_url = f"https://www.jobs.nhs.uk{detail_link['vacancy_detail_link']}"
            page.goto(detail_url)
            time.sleep(2)
            try:
                apply_link =  page.locator('div.buttons.standAlone a').get_attribute("href")
                apply_link = f"https://www.jobs.nhs.uk/{apply_link}"
            except:
                apply_link = ""
            if apply_link != "":
                try:
                    data = cur.execute(f"SELECT * FROM jobs WHERE job_ref = '{job_ref}'")
                    if not data > 0:
                        category_id = get_category_id(vacancy_category)
                        cur.execute(f'INSERT INTO `jobs`(`website_id`, `category_id`, `title`, `salary`, `job_ref`, `staff_group`, `description`, `apply_link`,`location`) VALUES ("1","{category_id}","{detail_link["vacancy_title"]}","{detail_link["salary"]}","{detail_link["job_ref"]}","{detail_link["staff_group"]}","{detail_link["description"]}","{apply_link}","{detail_link["location"]}")')
                        job_id = connection.insert_id()
                        connection.commit()
                        
                        job_type_id_get = job_type_id(job_type)
                        cur.execute(f"INSERT INTO `job_types`(`job_id`, `job_type_id`) VALUES ('{job_id}','{job_type_id_get}')")
                        connection.commit()
                except Exception as e:
                    print(e)
                    pass
connection.close() 