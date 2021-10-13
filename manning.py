#!venv/bin/python3

"""
Date:    Thu 07 Oct 2021 11:39:45 PM EDT
Author:  Bobak Kechavarzi <bdkech@gmail.com>
License: MIT
"""

import time
import datetime
import os
import errno
import click

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options


@click.group()
def main():
    pass

def _create_folder(folder):
    """
    Creates folder at the path for downloads
    """

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


@main.command()
@click.argument('username')
@click.argument('password')
@click.argument('folder')
def download_books(username, password, folder):
    base_url = 'https://www.manning.com'

    _create_folder(folder)

    limit = 5
    sortby = 'lastUpdated'

    options = Options()
    options.headless = True

    fp=webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList",2)
    fp.set_preference("browser.download.dir", folder)
    fp.set_preference("browser.download.panel.shown", False)
    fp.set_preference("browser.helperApps.neverAsk.openFile","text/csv,application/vnd.ms-excel")
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream");
    fp.set_preference("browser.download.manager.showWhenStarting", False);
    fp.set_preference("browser.download.manager.alertOnEXEOpen", False);
    fp.set_preference("browser.download.manager.focusWhenStarting", False);
    fp.set_preference("browser.download.folderList", 2);
    fp.set_preference("browser.download.useDownloadDir", True);
    fp.set_preference("browser.helperApps.alwaysAsk.force", False);
    fp.set_preference("browser.download.manager.alertOnEXEOpen", False);
    fp.set_preference("browser.download.manager.closeWhenDone", True);
    fp.set_preference("browser.download.manager.showAlertOnComplete", False);
    fp.set_preference("browser.download.manager.useWindow", False);
    fp.set_preference("services.sync.prefs.sync.browser.download.manager.showWhenStarting", False);
    fp.set_preference("pdfjs.disabled", True);

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

    rows = driver.find_elements_by_tag_name('tr')
    for row in rows:
        #print(row.find_elements_by_class_name('dropdown-toggle'))
        pdf_links = row.find_elements_by_partial_link_text('pdf')
        for pdf_link in pdf_links:
            pdf_link.click()
            dl_link = row.find_elements_by_css_selector("[href*='PDF']")
            if len(dl_link) == 1:
                dl_link[0].click()
            else:
                print("issues with link")


if __name__ == '__main__':
    main()
