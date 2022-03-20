
import logging

import re
from datetime import datetime
from time import sleep, time
from typing import List

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from python import Compatibility
from python.Database import Database
from python.global_variables import global_variables as gv
from python.model.Category import Category
from python.model.Price import Price
from python.model.Product import Product
from python.model.SubCategory import SubCategory


class Getir:

    category_list = []

    def __init__(self, headless=False, slow_mo=50):
        Compatibility.check_folder()
        self.set_logging()

        self.database = Database(gv.DATABASE_LOCATION, gv.DATABASE_NAME)

        

        pw = sync_playwright().start()
        self.browser = pw.chromium.launch(headless=headless, slow_mo=slow_mo)

        self.page = self.browser.new_page()
        
        self.load_category_from_db()  # load category, sub_category from database
        
    def set_logging(self):
        logging.basicConfig(filename=fr'log/log_{self.get_time()}.log',
                            level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
        logging.info("Logging is set")

    def get_time(self):
        return datetime.now().strftime("%H_%M_%S_%d_%m_%Y")

    def get_category_list(self) -> List[Category]:
        return self.category_list

    def load_category_from_db(self) -> List[Category]:
        self.category_list.clear()
        self.category_list = self.database.get_all_category()
        if len(self.category_list) == 0:
            logging.info("No category found in database")
            self.get_getir_category_with_sub_category()
        return self.category_list

    def get_getir_category_with_sub_category(self):
        self.get_category_from_web()
        for category in self.category_list:
            self.get_sub_category_from_web(category)

    def get_category_from_web(self):
        category_name = []
        self.page.goto(gv.GETIR_HOME)
        section_class_category = self.page.query_selector(
            'section[class^=style__CategoriesWrapper]')
        if section_class_category != None:
            html = section_class_category.inner_html()
            soup = BeautifulSoup(html, "html.parser")
            all_categories = soup.find_all("span")
            for category in all_categories:
                if (category.text != "") and (category.text not in category_name):
                    category_name.append(category.text)

            for category in category_name:
                if self.database.get_category_with_name(category) == None:
                    category_obj = Category(name=category)
                    self.database.add_category(category_obj)
                    logging.info(f"Category {category} added to database")
            self.load_category_from_db()

    def get_sub_category_from_web(self, category: Category):
        if (self.page.url == gv.GETIR_HOME):
            self.page.click(f'img[alt="{category.name}"]')
            dongu = True
            while dongu:
                all_query = self.page.query_selector_all(
                    "div[data-testid='breadcrumb-item']")
                for query in all_query:
                    if (query.inner_text() == category.name):
                        dongu = False
            panel_body = self.page.query_selector(
                'div[data-testid="panel-body"]')
            if panel_body != None:
                html = panel_body.inner_html()
                soup = BeautifulSoup(html, "html.parser")
                all_sub_categories = soup.find_all("a")
                for sub_category in all_sub_categories:
                    sub_category_span = sub_category.select(
                        'span[data-testid="text"]')[0].text
                    if self.database.get_sub_category_with_id_name(category.id, sub_category_span) == None:
                        sub_category_obj = SubCategory(name=sub_category_span)
                        self.database.add_sub_category(
                            sub_category_obj, category)
                        logging.info(
                            f"Sub Category {sub_category_span} added to database")

        elif ("https://getir.com/kategori/" in self.page.url):
            collapse_div = self.page.query_selector(
                'div[data-testid="collapse"]')
            panel_divs = collapse_div.query_selector_all(
                'div[data-testid="panel"]')
            for panel_div in panel_divs:
                span_text = panel_div.query_selector(
                    'span[data-testid="text"]').inner_text()
                if span_text == category.name:
                    panel_div.click()

                    panel_body = panel_div.query_selector(
                        'div[data-testid="panel-body"]')
                    if panel_body != None:
                        html = panel_body.inner_html()
                        soup = BeautifulSoup(html, "html.parser")
                        all_sub_categories = soup.find_all("a")
                        for sub_category in all_sub_categories:
                            sub_category_span = sub_category.select(
                                'span[data-testid="text"]')[0].text
                            if self.database.get_sub_category_with_id_name(category.id, sub_category_span) == None:
                                sub_category_obj = SubCategory(
                                    name=sub_category_span)
                                self.database.add_sub_category(
                                    sub_category_obj, category)
                                logging.info(
                                    f"Sub Category {sub_category_span} added to database")
                        break
        else:
            self.page.goto(gv.GETIR_HOME)
            self.get_sub_category_from_web(category)

    def get_sub_categories_with_category(self, category: Category) -> List[SubCategory]:
        return self.database.get_sub_categories(category)

    def get_getir_all_sub_category(self):
        for category in self.category_list:
            self.get_sub_category_from_web(category)

    def go_category(self, category: Category):
        if (self.page.url == gv.GETIR_HOME):
            # home screen
            self.page.click(f'img[alt="{category.name}"]')
            sleep(2)  # WAİT FOR PAGE LOAD WİTH PLAYWRIGHT NOT TIME.SLEEP
            self.page.query_selector(
                "div[name='category-products']").wait_for_element_state("visible")
            all_query = self.page.query_selector_all(
                "div[data-testid='breadcrumb-item']")
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
            # category page

            collapse_div = self.page.query_selector(
                'div[data-testid="collapse"]')
            panel_divs = collapse_div.query_selector_all(
                'div[data-testid="panel"]')
            for panel_div in panel_divs:
                span_text = panel_div.query_selector(
                    'span[data-testid="text"]').inner_text()
                if span_text == category.name:
                    panel_div.click()
        else:
            # not in category page
            self.page.goto(gv.GETIR_HOME)
            self.go_category(category)

    def go_sub_category(self, sub_category: SubCategory):
        category = self.database.get_category_with_sub_category(sub_category)
        if category != None:
            self.go_category(category)

            collapse_div = self.page.query_selector(
                'div[data-testid="collapse"]')
            panel_divs = collapse_div.query_selector_all(
                'div[data-testid="panel"]')
            for panel_div in panel_divs:
                span_text = panel_div.query_selector(
                    'span[data-testid="text"]').inner_text()
                if span_text == category.name:
                    panel_body = panel_div.query_selector(
                        'div[data-testid="panel-body"]')
                    if panel_body != None:
                        a_list = panel_body.query_selector_all('a')
                        for a in a_list:
                            span_text = a.query_selector(
                                'span[data-testid="text"]').inner_text()
                            if span_text == sub_category.name:
                                a.click()
                                break

    def clear_text_for_sql_injection(self, text: str) -> str:
        return text.replace("'", "").replace('"', "").replace("\\", "").replace("'", "").replace("é", "")

    def clear_price(self, price: str) -> float:
        return float(price.replace("₺", "").replace(",", "."))

    def get_all_getir_products(self, pass_yeni_urunler : bool = True, pass_indirimler : bool = True, pass_ilginizi_cekebilecekler : bool = True ):
        for category in self.category_list:
            self.page.goto(gv.GOOGLE)
            if pass_yeni_urunler and category.name == "Yeni Ürünler":
                print("Pass Yeni Ürünler")
                pass
            elif pass_indirimler and category.name == "İndirimler":
                print("Pass İndirimler")
                pass
            else:
                for sub_category in self.get_sub_categories_with_category(category):
                    if pass_ilginizi_cekebilecekler and sub_category.name == "İlginizi Çekebilecekler":
                        print("Pass İlginizi Çekebilecekler")
                        pass
                    else:
                        self.go_sub_category(sub_category)
                        self.get_product_list_web(sub_category)

    def get_card_wrapper(self, sub_category: SubCategory):
        self.page.query_selector(
            "div[name='category-products']").wait_for_element_state("visible")
        
        div_category_products = self.page.query_selector(
            "div[name='category-products']")
        
        div_list = div_category_products.query_selector_all("div")
        for div in div_list:
            header_div = div.query_selector(
                "div[class^='style__HeaderWrapper']")
            if header_div != None:
                h5_text = header_div.query_selector("h5").inner_text()
                if h5_text == sub_category.name:
                    card_wrapper = div.query_selector(
                        "div[class^='style__CardWrapper']")
                    html = card_wrapper.inner_html()
                    return html
            elif header_div == None:
                # header_div bulamıyorsan
                breadcrumb_item = self.page.query_selector_all(
                    "div[data-testid='breadcrumb-item']")[1].inner_text()
                if breadcrumb_item == sub_category.name:
                    print("BULDUM ONU")
                    selected_div = div_list[0]
                    card_wrapper = selected_div.query_selector(
                        "div[class^='style__CardWrapper']")
                    html = card_wrapper.inner_html()
                    return html


    def get_product_list_db(self, sub_category: SubCategory) -> List[Product]:
        return self.database.get_all_product(sub_category)

    def get_product_list_web(self, sub_category: SubCategory):
        """Get product list from web page with sub_category"""
        print(f"Getting product list with sub category {sub_category.name}")

        new_product_count = 0
        old_product_count = 0
        
        change_price_count = 0
        
        html = None
        category = self.database.get_category_with_sub_category(sub_category)
        
        if category != None:

            html = self.get_card_wrapper(sub_category)


            #TODO START
            # sub_category_list = category.get_sub_categories()
            
            # selected_index = 0
            # for index, sub_category_f in enumerate(sub_category_list):
            #     if (sub_category_f.name == sub_category.name):
            #         selected_index  = index
            #         break
            
            # div_category_products = self.page.query_selector(
            #     "div[name='category-products']")
            # div_list = div_category_products.query_selector_all("div")
            # selected_div = div_list[selected_index]
            # card_wrapper = selected_div.query_selector(
            #     "div[class^='style__CardWrapper']")
            # if card_wrapper == None:
            #     print("wtf")
            # else:
            #     html = card_wrapper.inner_html()
            #BU ŞEKİLDE İLK 2 DIVDE ÇALIŞIYOR SONRA ÇALIŞMIYOR FAKAT DAHA HIZLI ÇALIŞIYOR. 
            #TODO STOP

            if html != None:
                soup = BeautifulSoup(html, "html.parser")
                all_product_article = soup.find_all("article")
                for product_article in all_product_article:
                    has_discount = False
                    discount_price = "0"
                    
                    div_price_wrapper = product_article.select(
                        "div[class^='style__PriceWrapper']")[0]
                    
                    price = div_price_wrapper.select("span")
                    
                    if len(price) == 1:
                        original_price = price[0].text
                    elif len(price) == 2: # indirimli ürün 2 fiyat var
                        original_price = price[0].text
                        has_discount = True
                        discount_price = price[1].text
                    else:
                        logging.error("Price not found")
                        original_price = "0"
                        
                    discount_price = self.clear_price(discount_price)
                    original_price = self.clear_price(original_price)

                    # price = div_price_wrapper.select("span")[0].text #OK

                    div_paragraph = product_article.select(
                        "div[data-testid='paragraph']")[0]
                    p_paragraph = div_paragraph.select("p")[0].text  # OK
                    p_paragraph = self.clear_text_for_sql_injection(
                        p_paragraph)

                    span_text = product_article.select(
                        "span[data-testid='text']")
                    if len(span_text) == 2:
                        span_text = span_text[1].text
                    elif len(span_text) == 3:
                        span_text = span_text[2].text
                    # span_text = product_article.select("span[data-testid='text']")[1].text
                    # check span text

                    span_text = self.clear_text_for_sql_injection(span_text)

                    product_obj = Product(name=span_text, description=p_paragraph,
                                          sub_category_id=sub_category.id, category_id=category.id)
                    database_product = self.database.get_product_id_with_name_description(
                        product_obj.name, product_obj.description)
                    if database_product == None:
                        self.database.add_product(product_obj)
                        new_product_count += 1
                        logging.info(f"Product {span_text} added to database")
                    else:
                        old_product_count += 1
                        product_obj.id = database_product.id

                    last_price = self.database.get_last_price(product_obj)
                    if last_price == None:
                        price_obj = Price(
                            price_value=original_price, product_id=product_obj.id, time_unix=time(), has_discount=has_discount, discount_price=discount_price)
                        self.database.add_price(price_obj)
                        if has_discount:
                            print(
                                f"Name: {span_text} {p_paragraph}, original price: {original_price}, discount price: {discount_price}")
                        else:
                            print(
                                f"Name: {span_text} {p_paragraph}, price: {original_price}₺")
                    elif last_price.price_value != original_price:
                        price_obj = Price(
                            price_value=original_price, product_id=product_obj.id, time_unix=time(), has_discount=has_discount, discount_price=discount_price)
                        self.database.add_price(price_obj)
                        change_price_count += 1
                        print(
                            f"Name: {span_text} {p_paragraph}, price: {original_price}₺, old price: {last_price.price_value}₺")


            print(f"{sub_category.name} new product count: {new_product_count}, old product count: {old_product_count}, change price count: {change_price_count}")
            logging.info(f"{category.name}/{sub_category.name} new product count: {new_product_count}, old product count: {old_product_count}, change price count: {change_price_count}")