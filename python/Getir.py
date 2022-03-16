
from typing import List
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime


from python.global_variables import global_variables as gv
from python import Compatibility 
from python.Database import Database

import re
import logging

from python.model.Category import Category
from python.model.SubCategory import SubCategory


class Getir:
    
    category_list = []

    def __init__(self, headless = False, slow_mo = 50):
        Compatibility.check_folder()
        self.set_logging()

        self.database = Database(gv.DATABASE_LOCATION, gv.DATABASE_NAME)

        self.load_category_list()


        pw = sync_playwright().start()
        self.browser = pw.chromium.launch(headless=headless,slow_mo= slow_mo)

        self.page = self.browser.new_page()

    def get_time_log_config(self):
        return datetime.now().strftime("%H_%M_%S_%d_%m_%Y")

    def load_category_list(self) -> List[Category]:
        self.category_list.clear()
        self.category_list = self.database.get_all_category()
        return self.category_list

    def get_getir_category(self):
        category_name = []
        self.page.goto(gv.GETIR_HOME)
        section_class_category = self.page.query_selector('section[class^=style__CategoriesWrapper]')
        if section_class_category != None:
            html = section_class_category.inner_html()
            soup = BeautifulSoup(html,"html.parser")
            all_categories = soup.find_all("span")
            for category in all_categories:
                if (category.text != "") and (category.text not in category_name):
                    category_name.append(category.text)
                
            for category in category_name:
                if self.database.get_category_with_name(category) == None:
                    category_obj = Category(name = category)
                    self.database.add_category(category_obj)
                    logging.info(f"Category {category} added to database")
            self.load_category_list()

                
            
    def get_getir_sub_category(self,category:Category):
        if (self.page.url == gv.GETIR_HOME):
            #find category name and click
            self.page.click(f'img[alt="{category.name}"]')

            dongu = True
            while dongu:
                all_query = self.page.query_selector_all("div[data-testid='breadcrumb-item']")
                for query in all_query:
                    if (query.inner_text() == category.name):
                        self.page.screenshot(path=f'img/{category.name}.png')
                        dongu = False
            panel_body = self.page.query_selector('div[data-testid="panel-body"]')
            if panel_body != None:
                html = panel_body.inner_html()
                soup = BeautifulSoup(html,"html.parser")
                all_sub_categories = soup.find_all("a")
                for sub_category in all_sub_categories:
                    sub_category_span = sub_category.select('span[data-testid="text"]')[0].text
                    if self.database.get_sub_category_with_category_id_and_name(category.id,sub_category_span) == None:
                        sub_category_obj = SubCategory(name = sub_category_span)
                        self.database.add_sub_category(sub_category_obj,category)
                        logging.info(f"Sub Category {sub_category_span} added to database")

                

            

        elif ("https://getir.com/kategori/" in self.page.url):
            #already in category find sub category of category name
            pass
        else:
            #not in category page
            self.page.goto(gv.GETIR_HOME)
            self.get_getir_sub_category(category)

    
    def get_getir_all_sub_category(self):
        for category in self.category_list:
            self.get_getir_sub_category(category)

    #TODO GETİR FAVORİ ÜRÜNLERİ ÇEK

    def set_logging(self):
        logging.basicConfig(filename=fr'log/log_{self.get_time_log_config()}.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
        logging.info("Logging is set")
    
        
    
