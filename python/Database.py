
import sqlite3 as sql

from os import getcwd
from typing import List

from python.model.Category import Category
from python.model.Price import Price
from python.model.Product import Product
from python.model.SubCategory import SubCategory
from python.global_variables import global_variables as gv

import logging

class Database:
    location = None
    name = None

    category_list = []
    len_category_list = 0
    len_sub_category_list = 0
    
    product_list = []
    product_count = 0
    def __init__(self, location, name) -> None:
        
        self.name = name
        self.location = getcwd() + "\\"+location + "\\" + name + ".db"
        self.check_database()
        logging.info("Database initialized. Database Location: " + self.location)

    def check_database(self):
            self.create_table(gv.CREATE_CATEGORY_TABLE_QUERY,"category")
            self.create_table(gv.CREATE_PRODUCT_TABLE_QUERY,"product")
            self.create_table(gv.CREATE_SUB_CATEGORY_TABLE_QUERY,"sub_category")
            self.create_table(gv.CREATE_PRICE_TABLE_QUERY,"price")

    def create_table(self,sql_query, table_name = "unknown"):
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        self.im.execute(sql_query)
        self.db.commit()
        logging.info("Table created. Table Name: " + table_name)
        self.db.close()

    def get_category_with_name(self,name) -> Category:
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        self.im.execute(f"SELECT * FROM category WHERE name = '{name}'")
        returnValue = self.im.fetchone()
        if returnValue == None:
            return None
        id, name, description = returnValue #CATEGORY model değişirse unutma
        if description == 'None':
            description = None
        category = Category(id,name,description)
        self.db.close()
        return category
    
    def get_table_names(self) -> List[str]:
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        self.im.execute("SELECT name FROM sqlite_master")
        tableNames = self.im.fetchall()
        newTableNames = []
        for i in tableNames:
            i = str(i).replace("(","").replace(")","").replace("'","").replace(",","")
            newTableNames.append(i)
        tableNames = newTableNames
        self.db.close()
        return tableNames
    
    def check_table_names(self,table_name) -> bool:
        tableNames = self.get_table_names()
        if table_name in tableNames:
            return True
        else:
            return False

    def get_all_category(self) -> List[Category]:
        """Get all Category"""
        self.len_category_list = 0
        self.len_sub_category_list = 0
        self.category_list.clear()
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        self.im.execute("SELECT * FROM category")
        allDb = self.im.fetchall()

        for i in allDb:
            id, name, description = i #CATEGORY model değişirse unutma
            if description == 'None':
                description = None
            category = Category(id,name,description)
            
            sub_category_list = self.get_sub_categories(category)
            category.set_sub_categories(sub_category_list)
            self.len_sub_category_list += category.get_len_sub_categories()
            self.category_list.append(category)
            self.len_category_list += 1
        self.db.close()
        logging.info(f"Category table fetched Lenght: {self.len_category_list}, sub_category table fetched Lenght: {self.len_sub_category_list}")
        return self.category_list
    
    def get_sub_category_with_id_name(self,category_id,name) -> SubCategory:
        """Get SubCategory with id and name"""
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        self.im.execute(f"SELECT * FROM sub_category WHERE category_id={category_id} AND name='{name}'")
        returnValue = self.im.fetchone()
        if returnValue == None:
            return None
        id,  name, description , category_id = returnValue #SUB_CATEGORY model değişirse unutma
        if description == 'None':
            description = None
        sub_category = SubCategory(id,category_id,name,description)
        self.db.close()
        return sub_category

    def get_sub_categories(self,category : Category) -> List[SubCategory]:
        """Get SubCategory with Category(ID)"""
        sub_category_list = []
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        self.im.execute(f"SELECT * FROM sub_category WHERE category_id={category.id}")
        returnValue = self.im.fetchall()
        for sub_category in returnValue:
            id,  name, description , category_id = sub_category
            if description == 'None':
                description = None
            sub_category = SubCategory(id,name,description,category_id)
            sub_category_list.append(sub_category)
        self.db.close()
        return sub_category_list

    def get_category_with_sub_category(self,sub_category : SubCategory) -> Category:
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        self.im.execute(f"SELECT * FROM category WHERE id={sub_category.category_id}")
        returnValue = self.im.fetchone()
        if returnValue == None:
            return None
        id, name, description = returnValue #CATEGORY model değişirse unutma
        if description == 'None':
            description = None
        category = Category(id,name,description)
        sub_category_list = self.get_sub_categories(category)
        category.set_sub_categories(sub_category_list)
        self.db.close()
        return category

    def add_category(self,category : Category):
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()

        VALUES = f"""
        '{category.name}',
        '{category.description}'
        """
        
        self.im.execute(f"INSERT INTO category({gv.ADD_CATEGORY_KEY}) VALUES({VALUES})")
        category.id = self.im.lastrowid
        self.db.commit()
        self.db.close()
        logging.info(f"Category added. Category Name: {category.name}")

    def add_sub_category(self,
                        sub_category:SubCategory,
                        category:Category):
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        VALUES = f"""
        '{sub_category.name}',
        '{sub_category.description}',
        {category.id}
        """
        self.im.execute(f"INSERT INTO sub_category({gv.ADD_SUB_CATEGORY_KEY}) VALUES({VALUES})")
        sub_category.id = self.im.lastrowid
        self.db.commit()
        self.db.close()
        logging.info(f"{sub_category.name} sub category added for {category.name}.")

    def add_product(self,product:Product):
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        VALUES = f"""
        '{product.name}',
        '{product.description}',
        {product.category_id},
        {product.sub_category_id}
        """
        self.im.execute(f"INSERT INTO product({gv.ADD_PRODUCT_KEY}) VALUES({VALUES})")
        product.set_id(self.im.lastrowid)
        self.db.commit()
        self.db.close()
        logging.info("Product added. Product Name: " + product.name)
        return self.im.lastrowid

    def add_price(self, price:Price):
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        VALUES = f"""
        {price.price_value},
        {price.product_id},
        {price.time_unix},
        {price.has_discount},
        {price.discount_price}
        """
        self.im.execute(f"INSERT INTO price({gv.ADD_PRICE_KEY}) VALUES({VALUES})")
        price.id = self.im.lastrowid
        self.db.commit()
        self.db.close()
        return price

    def get_product_id_with_name_description(self,name:str,description:str) -> Product | None:
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        try:
            self.im.execute(f"SELECT * FROM product WHERE name='{name}' AND description='{description}'")
        except Exception as e :
            print(f"Name: {name}, Desc: {description} Error: {e}")
            return None
        returnValue =self.im.fetchone()
        if returnValue == None:
            return None
        else:
            #CREATE_PRODUCT_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS product (id INTEGER PRIMARY KEY, name TEXT NOT NULL, description TEXT, category_id INTEGER, sub_category_id INTEGER);"""
            id, name, description, category_id, sub_category_id = returnValue
            product = Product(id,name,description,category_id,sub_category_id)
            self.db.close()
            return product

    def get_last_price(self,product : Product) -> Price:
        
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        self.im.execute(f"SELECT * FROM price WHERE product_id={product.id} ORDER BY time_unix DESC LIMIT 1")
        returnValue = self.im.fetchone()
        if returnValue == None:
            return None
        id, price_value, product_id, time_unix, has_discount, discount_price = returnValue
        
        if has_discount == 0:
            has_discount = False
        else:
            has_discount = True
            
        price = Price(id,price_value,product_id,time_unix,has_discount,discount_price)
        self.db.close()
        return price

    def get_product_w_sub_category(self,sub_category:SubCategory) -> List[Product]:
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        self.im.execute(f"SELECT * FROM product WHERE sub_category_id={sub_category.id}")
        returnValue = self.im.fetchall()
        self.product_list = []
        self.product_count = 0
        for product in returnValue:
            id, name, description, category_id, sub_category_id = product
            product = Product(id,name,description,category_id,sub_category_id)
            product.set_price(self.get_last_price(product))
            self.product_list.append(product)
        self.db.close()
        return self.product_list
    
    def get_all_product(self) -> List[Product]:
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        self.im.execute(f"SELECT * FROM product")
        returnValue = self.im.fetchall()
        self.product_list = []
        self.product_count = 0
        for product in returnValue:
            id, name, description, category_id, sub_category_id = product
            product = Product(id,name,description,category_id,sub_category_id)
            product.set_price(self.get_last_price(product))
            self.product_list.append(product)
        self.db.close()
        return self.product_list