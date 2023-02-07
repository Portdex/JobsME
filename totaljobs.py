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
os.environ["BROWSER_PATH"] = "~/.cache/ms-playwright"
