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

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options

# Defaults
limit = 5
sortby = 'lastUpdated'
options = Options()
options.headless = True

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
# If you want to open Firefox
        driver = webdriver.Firefox(options=options, service_log_path='/dev/null')

        driver.get('https://login.manning.com/login?service=https%3A%2F%2Fwww.manning.com%2Flogin%2Fcas')
        username_ele = driver.find_element_by_id("username-sign-in")
        password_ele = driver.find_element_by_id("password-sign-in")
        username_ele.send_keys(username)
        password_ele.send_keys(password)
        driver.find_element_by_name("submit").click()
        time.sleep(4)
        driver.get('https://www.manning.com/dashboard/index?filter=all&order=purchaseDate&sort=asc')
        page_source = driver.page_source
        print(page_source)
        # PURPOSE: Parse the dashboard with up to 999 products
        soup = BeautifulSoup(page_source, 'html.parser')
        div_container = soup.find('table', {'id': 'productTable'})
        print(div_container)
        for product in div_container.find_all('tr', {'class': 'license-row'}):
            # EXAMPLE: Terraform in Action
            title = str(product.find(
                'div', {'class': 'product-title'}).text.strip())
            # PURPOSE: Find all the restrictedDownloadIds and create a complete payload
            for downloadSelection in product.find_all('div', {'class': 'download-selection'}):
                hidden = downloadSelection.find_all(
                    'input', {'type': 'hidden'})
                for val in hidden:
                    checkbox1 = (val['id'], val['value'])
                    checkbox2 = (restrictedDownloadIds, val['id'])
                    download_payload.append(checkbox1)
                    download_payload.append(checkbox2)
                    # EXAMPLE: [('dropbox', 'false'), ('productExternalId', 'winkler'), ('1971', '7850702'), ('winkler-restrictedDownloadIds', '1971'), ('1972', '7850703'), ('winkler-restrictedDownloadIds', '1972'), ('1973', '7850704'), ('winkler-restrictedDownloadIds', '1973')]
            try:
                subfolder = str(title.replace(' ', '_'))
                path = os.path.join(folder, subfolder)
                os.makedirs(path)
                print('Created folder', path)
            except OSError as e:
                if e.errno == errno.EEXIST:
                    print(f'Directory {path} already exists.')
                else:
                    raise
            downloadURL = 'https://www.manning.com/dashboard/download?id=downloadForm-' + author
            print('Downloading', title, '...')
            dl = s.post(downloadURL, cookies=s.cookies,
                        headers=headers, data=download_payload)
            # PURPOSE: Some free titles are only in PDF format, this can be determined from the amount of hidden inputs
            if len(download_payload) <= 4:
                extension = '.pdf'
            else:
                extension = '.zip'
            filename = path + '/' + subfolder + extension
            file = open(filename, "wb")
            file.write(dl.content)
            file.close()

def end_script():
    print('Exiting the script...')
    sys.exit()


if len(sys.argv) > 1:
    main(sys.argv[1:])
    # create_folder()
    get_list()
    end_script()
else:
    print('Help: `manning.py -h`')
    sys.exit()
