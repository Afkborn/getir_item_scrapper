
from typing import List
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime


from python.global_variables import global_variables as gv
from python import Compatibility 
from python.Database import Database

import re
import logging
from time import sleep, time

from python.model.Category import Category
from python.model.SubCategory import SubCategory
from python.model.Price import Price
from python.model.Product import Product

class Getir:
    
    category_list = []

    def __init__(self, headless = False, slow_mo = 50):
        Compatibility.check_folder()
        self.set_logging()

        self.database = Database(gv.DATABASE_LOCATION, gv.DATABASE_NAME)

        self.load_category_list_from_database()


        pw = sync_playwright().start()
        self.browser = pw.chromium.launch(headless=headless,slow_mo= slow_mo)

        self.page = self.browser.new_page()

    def get_time_log_config(self):
        return datetime.now().strftime("%H_%M_%S_%d_%m_%Y")

    def get_category_list(self) -> List[Category]:
        return self.category_list

    def load_category_list_from_database(self) -> List[Category]:
        self.category_list.clear()
        self.category_list = self.database.get_all_category()
        return self.category_list

    def get_getir_category_with_sub_category(self):
        self.get_getir_category_from_web()
        for category in self.category_list:
            self.get_getir_sub_category(category)

    def get_getir_category_from_web(self):
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
            self.load_category_list_from_database()

                
    def get_getir_sub_category(self,category:Category):
        if (self.page.url == gv.GETIR_HOME):
            self.page.click(f'img[alt="{category.name}"]')

            dongu = True
            while dongu:
                all_query = self.page.query_selector_all("div[data-testid='breadcrumb-item']")
                for query in all_query:
                    if (query.inner_text() == category.name):
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
            collapse_div = self.page.query_selector('div[data-testid="collapse"]')
            panel_divs = collapse_div.query_selector_all('div[data-testid="panel"]')
            for panel_div in panel_divs:
                span_text = panel_div.query_selector('span[data-testid="text"]').inner_text()
                if span_text == category.name:
                    panel_div.click()

                    panel_body = panel_div.query_selector('div[data-testid="panel-body"]')
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
                        break

        else:
            #not in category page
            self.page.goto(gv.GETIR_HOME)
            self.get_getir_sub_category(category)

    def get_sub_category_with_category(self, category : Category) -> List[SubCategory]:
        return self.database.get_sub_category_with_category(category)
    
    def get_getir_all_sub_category(self):
        for category in self.category_list:
            self.get_getir_sub_category(category)

    def go_category(self, category : Category):
        if (self.page.url == gv.GETIR_HOME):
            #home screen
            self.page.click(f'img[alt="{category.name}"]')
            sleep(2) # WAİT FOR PAGE LOAD WİTH PLAYWRIGHT NOT TIME.SLEEP
            self.page.query_selector("div[name='category-products']").wait_for_element_state("visible")
            all_query = self.page.query_selector_all("div[data-testid='breadcrumb-item']")
            for query in all_query:
                if (query.inner_text() == category.name):
                    break
            # dongu = True
            # while dongu:
            #     all_query = self.page.query_selector_all("div[data-testid='breadcrumb-item']")
            #     for query in all_query:
            #         if (query.inner_text() == category.name):
            #             dongu = False
        elif ("https://getir.com/kategori/" in self.page.url):
            #category page
            collapse_div = self.page.query_selector('div[data-testid="collapse"]')
            panel_divs = collapse_div.query_selector_all('div[data-testid="panel"]')
            for panel_div in panel_divs:
                span_text = panel_div.query_selector('span[data-testid="text"]').inner_text()
                if span_text == category.name:
                    panel_div.click()
        else:
            #not in category page
            self.page.goto(gv.GETIR_HOME)
            self.go_category(category)


    def go_sub_category(self,sub_category:SubCategory):
        category = self.database.get_category_with_sub_category(sub_category)
        if category != None:
            self.go_category(category)

            collapse_div = self.page.query_selector('div[data-testid="collapse"]')
            panel_divs = collapse_div.query_selector_all('div[data-testid="panel"]')
            for panel_div in panel_divs:
                span_text = panel_div.query_selector('span[data-testid="text"]').inner_text()
                if span_text == category.name:
                    panel_body = panel_div.query_selector('div[data-testid="panel-body"]')
                    if panel_body != None:
                        a_list = panel_body.query_selector_all('a')
                        for a in a_list:
                            span_text = a.query_selector('span[data-testid="text"]').inner_text()
                            if span_text == sub_category.name:
                                a.click()
                                break
    
    def clear_text_for_sql_injection(self,text:str) -> str:
        return text.replace("'","").replace('"',"").replace("\\","").replace("'","").replace("é","")

    def clear_price(self,price:str) -> float:
        return float(price.replace("₺","").replace(",","."))

    def get_product_list_with_sub_category(self,sub_category:SubCategory):
        print(f"Getting product list with sub category {sub_category.name}")
        
        product_count = 0

        html = None
        category = self.database.get_category_with_sub_category(sub_category)
        if category != None:
            self.page.query_selector("div[name='category-products']").wait_for_element_state("visible")
            div_category_products = self.page.query_selector("div[name='category-products']")
            div_list = div_category_products.query_selector_all("div")
            for div in div_list:
                header_div = div.query_selector("div[class^='style__HeaderWrapper']")
                if header_div != None:
                    h5_text = header_div.query_selector("h5").inner_text()
                    if h5_text == sub_category.name:
                        card_wrapper = div.query_selector("div[class^='style__CardWrapper']")
                        html = card_wrapper.inner_html()
                        break
                elif header_div == None:
                    #header_div bulamıyorsan
                    breadcrumb_item = self.page.query_selector_all("div[data-testid='breadcrumb-item']")[1].inner_text()
                    if breadcrumb_item == sub_category.name:
                        print("BULDUM ONU")
                        selected_div = div_list[0]
                        card_wrapper = selected_div.query_selector("div[class^='style__CardWrapper']")
                        html = card_wrapper.inner_html()
                        break

                
            if html != None:
                soup = BeautifulSoup(html,"html.parser")
                all_product_article = soup.find_all("article")
                for product_article in all_product_article:

                        div_price_wrapper = product_article.select("div[class^='style__PriceWrapper']")[0]
                        price = div_price_wrapper.select("span")
                        if len(price) == 1:
                            price_text = price[0].text
                        elif len(price) == 2:
                            price_text = price[1].text
                        else:
                            print("price wtf")
                            price_text = "0"
                        price_text = self.clear_price(price_text)

                        #price = div_price_wrapper.select("span")[0].text #OK

                        div_paragraph = product_article.select("div[data-testid='paragraph']")[0]
                        p_paragraph = div_paragraph.select("p")[0].text #OK
                        p_paragraph = self.clear_text_for_sql_injection(p_paragraph)

                        span_text = product_article.select("span[data-testid='text']")
                        if len(span_text) == 2:
                            span_text = span_text[1].text
                        elif len(span_text) == 3:
                            span_text = span_text[2].text
                            print(f"indirimli ürün {span_text}")
                        # span_text = product_article.select("span[data-testid='text']")[1].text
                        #check span text 

                        
                        span_text = self.clear_text_for_sql_injection(span_text)

                        product_obj =  Product(name=span_text,description=p_paragraph,sub_category_id=sub_category.id, category_id=category.id)
                        database_product = self.database.get_product_id_with_name_description(product_obj.name,product_obj.description)
                        if database_product == None:
                            self.database.add_product(product_obj)
                            product_count += 1
                            logging.info(f"Product {span_text} added to database")
                        else:
                            product_obj.id = database_product.id

                        

                        last_price = self.database.get_last_price_of_product(product_obj)
                        if last_price == None:
                            price_obj = Price(price_value=price_text,product_id=product_obj.id,time_unix=time())
                            self.database.add_price(price_obj)

                        elif  last_price.price_value != price:
                            price_obj = Price(price_value=price_text,product_id=product_obj.id,time_unix=time())
                            self.database.add_price(price_obj)

                        print(f"Name: {span_text} Price: {price_text} Paragraph: {p_paragraph}")
        print(f"{sub_category.name} product count: {product_count}")

    




    def set_logging(self):
        logging.basicConfig(filename=fr'log/log_{self.get_time_log_config()}.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
        logging.info("Logging is set")
    

    
        
    
