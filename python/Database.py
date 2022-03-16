from calendar import c
import sqlite3 as sql
from os.path import exists
from os import getcwd
from typing import List

from python.model.Category import Category
from python.model.Product import Product
from python.model.SubCategory import SubCategory
from python.global_variables import global_variables as gv

import logging

class Database:
    location = None
    name = None

    category_list = []
    len_category_list = 0

    def __init__(self, location, name) -> None:
        
        self.name = name
        self.location = getcwd() + "\\"+location + "\\" + name + ".db"
        self.check_database()
        logging.info("Database initialized. Database Location: " + self.location)

    def check_database(self):
            self.create_table(gv.CREATE_CATEGORY_TABLE_QUERY,"category")
            self.create_table(gv.CREATE_PRODUCT_TABLE_QUERY,"product")
            self.create_table(gv.CREATE_SUB_CATEGORY_TABLE_QUERY,"sub_category")



    def create_table(self,sql_query, table_name = "unknown"):
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        self.im.execute(sql_query)
        self.db.commit()
        logging.info("Table created. Table Name: " + table_name)
        self.db.close()

    def get_category_with_id(self,id) -> Category:
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        self.im.execute(f"SELECT * FROM category WHERE id={id}")
        returnValue = self.im.fetchone()
        if returnValue == None:
            return None
        id, name, description = returnValue      #CATEGORY model değişirse unutma
        if description == 'None':
            description = None
        category = Category(id,name,description)
        self.db.close()
        return category

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

    def add_category(self,category : Category):
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        KEY = f"name,description"
        VALUES = f"""
        '{category.name}',
        '{category.description}'
        """
        self.im.execute(f"INSERT INTO category({KEY}) VALUES({VALUES})")
        category.id = self.im.lastrowid
        self.db.commit()
        self.db.close()
        logging.info("Category added. Category Name: " + category.name)
    
    def delete_category_with_id(self,id):
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        self.im.execute(f"DELETE FROM category WHERE id={id}")
        self.db.commit()
        self.db.close()
    
    def delete_category(self,category : Category):
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        self.im.execute(f"DELETE FROM category WHERE id={category.id}")
        self.db.commit()
        logging.info("Category deleted. Category Name: " + category.name)
        self.db.close()
    
    def get_table_names(self):
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

    def get_all_category(self):
        self.category_list.clear()

        tableNames = self.get_table_names()
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        if "category" in tableNames : 
            self.im.execute("SELECT * FROM category")
            allDb = self.im.fetchall()
            for i in allDb:
                id, name, description = i #CATEGORY model değişirse unutma
                if description == 'None':
                    description = None
                category = Category(id,name,description)

                sub_category_list = self.get_sub_category_with_category(category)
                category.sub_category_list = sub_category_list
                
                self.category_list.append(category)
                self.len_category_list += 1
        else:
            self.create_table(gv.CREATE_CATEGORY_TABLE_QUERY)
        self.db.close()
        logging.info(f"Category table fetched Lenght: {self.len_category_list}")
        return self.category_list

    def update_category(self,category : Category):
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        self.im.execute(f"UPDATE category SET name='{category.name}',description='{category.description}' WHERE id={category.id}")
        self.db.commit()
        logging.info("Category updated. Category Name: " + category.name)
        self.db.close()
    
    def get_lenght_category_table(self):
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        self.im.execute("SELECT * FROM category")
        lenght = self.im.fetchall()
        self.db.close()
        return len(lenght)
    
    def get_sub_category_with_category_id_and_name(self,category_id,name) -> SubCategory:
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

    def get_sub_category_with_category(self,category : Category) -> List[SubCategory]:
        sub_category_list = []
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        self.im.execute(f"SELECT * FROM sub_category WHERE category_id={category.id}")
        returnValue = self.im.fetchall()
        for sub_category in returnValue:
            id,  name, description , category_id = sub_category
            if description == 'None':
                description = None
            print(name)
            sub_category = SubCategory(id,name,description,category_id)
            sub_category_list.append(sub_category)
        self.db.close()
        return sub_category_list


    def add_sub_category(self,
                        sub_category:SubCategory,
                        category:Category):
        self.db = sql.connect(self.location)
        self.im = self.db.cursor()
        KEY = f"name,description,category_id"
        VALUES = f"""
        '{sub_category.name}',
        '{sub_category.description}',
        {category.id}
        """
        self.im.execute(f"INSERT INTO sub_category({KEY}) VALUES({VALUES})")
        sub_category.id = self.im.lastrowid
        self.db.commit()
        self.db.close()
        logging.info("Sub Category added. Sub Category Name: " + sub_category.name)

