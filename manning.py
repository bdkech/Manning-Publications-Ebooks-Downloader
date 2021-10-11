#!venv/bin/python3

"""
Date:    Thu 07 Oct 2021 11:39:45 PM EDT
Author:  Bobak Kechavarzi <bdkech@gmail.com>
License: MIT
"""

from bs4 import BeautifulSoup
import time
import datetime
import os
import errno
import sys
import getopt
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

# Defaults
limit = 5
sortby = 'lastUpdated'
options = Options()
options.headless = False
fp=webdriver.FirefoxProfile()
fp.set_preference("browser.helperApps.neverAsk.openFile", 'application/pdf')
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", 'application/pdf')
fp.set_preference("browser.download.panel.shown", False)
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir", "~/Downloads/")

def main(argv):
    global username
    global password
    global limit
    global sortby
    username = ''
    password = ''
    try:
        opts, args = getopt.getopt(
            argv, "hu:p:", ["username=", "password=", "limit=", "sort-by="])
    except getopt.GetoptError:
        print(
            'Usage: `manning.py -u <EMAIL> -p <PASSWORD> [--limit <1-999>] [--sort-by <title,purchaseDate,lastUpdated>]`')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(
                'Usage: `manning.py -u <EMAIL> -p <PASSWORD> [--limit <1-999>] [--sort-by <title,purchaseDate,lastUpdated>]`')
            sys.exit()
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("--limit"):
            limit = arg
            if not limit.isdigit():
                print('Not an integer 1-999!')
                sys.exit()
        elif opt in ("--sort-by"):
            sortby = arg
            if (not sortby == 'title') and (not sortby == 'purchaseDate') and (not sortby == 'lastUpdated'):
                print(
                    'Wrong option. Must be one of the following: `title`, `purchaseDate` or `lastUpdated`')
                sys.exit()
        else:
            print('Help: `manning.py -h`')
            sys.exit()


def create_folder():
    global folder
    datetime_object = datetime.date.today()
    folder = 'Manning_' + str(datetime_object)
    try:
        os.mkdir(folder)
        print('Created folder', folder)
    except OSError as e:
        if e.errno == errno.EEXIST:
            print(f'Directory {folder} already exists.')
        else:
            raise


def get_list():
        base_url = 'https://www.manning.com'
# If you want to open Firefox
        driver = webdriver.Firefox(firefox_profile=fp, options=options, service_log_path='/dev/null')

        driver.get('https://login.manning.com/login?service=https%3A%2F%2Fwww.manning.com%2Flogin%2Fcas')
        username_ele = driver.find_element_by_id("username-sign-in")
        password_ele = driver.find_element_by_id("password-sign-in")
        username_ele.send_keys(username)
        password_ele.send_keys(password)
        driver.find_element_by_name("submit").click()
        time.sleep(5)
        driver.get('https://www.manning.com/dashboard/index?filter=all&order=purchaseDate&sort=asc')
        time.sleep(5)
        dl_links = driver.find_elements_by_css_selector("[href*='PDF']")
        for dl_link in dl_links:
            print(dl_link.get_attribute('href'))
        driver.get(dl_link.get_attribute('href'))

if len(sys.argv) > 1:
    main(sys.argv[1:])
    create_folder()
    get_list()
else:
    print('Help: `manning.py -h`')
    sys.exit()
