
FOLDER_NAME= ["log","img","db"]


#URL
GETIR_HOME = "https://getir.com/"


#DATABASE
ADD_PRODUCT_KEY = "name,description,category_id,sub_category_id"
ADD_SUB_CATEGORY_KEY = "name,description,category_id"
ADD_CATEGORY_KEY = "name,description"
ADD_PRICE_KEY = "price_value,product_id,time_unix"
DATABASE_LOCATION = "db/"
DATABASE_NAME = "getir"
CREATE_CATEGORY_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS category (id INTEGER PRIMARY KEY, name TEXT NOT NULL,description TEXT );"""
CREATE_PRODUCT_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS product (id INTEGER PRIMARY KEY, name TEXT NOT NULL, description TEXT, category_id INTEGER, sub_category_id INTEGER);"""
CREATE_SUB_CATEGORY_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS sub_category (id INTEGER PRIMARY KEY, name TEXT NOT NULL,description TEXT,category_id INTEGER NOT NULL);"""
CREATE_PRICE_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS price (id INTEGER PRIMARY KEY, price_value REAL NOT NULL, product_id INTEGER NOT NULL, time_unix REAL NOT NULL);"""