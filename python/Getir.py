from numpy import rint
from playwright.sync_api import sync_playwright

from python.global_variables import global_variables as gv
from python import Compatibility 
import logging

from datetime import datetime
import re

from bs4 import BeautifulSoup

class Getir:
    
    def __init__(self, country_telephone_code, telephone_number, headless = False, slow_mo = 50):
        Compatibility.check_folder()
        self.set_logging()

        self.country_telephone_code = country_telephone_code
        self.telephone_number = telephone_number

        pw = sync_playwright().start()
        self.browser = pw.chromium.launch(headless=headless,slow_mo= slow_mo)

        self.page = self.browser.new_page()

    def get_time_log_config(self):
        return datetime.now().strftime("%H_%M_%S_%d_%m_%Y")

    def get_getir_category(self):
        self.category = []
        self.page.goto('https://getir.com/')

        section_class_category = self.page.query_selector('section[class^=style__CategoriesWrapper]')
        if section_class_category != None:
            html = section_class_category.inner_html()
            soup = BeautifulSoup(html,"html.parser")
            all_categories = soup.find_all("span")
            for category in all_categories:
                self.category.append(category.text)


    def set_logging(self):
        logging.basicConfig(filename=fr'log/log_{self.get_time_log_config()}.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
        logging.info("Logging is set")
    
        
    