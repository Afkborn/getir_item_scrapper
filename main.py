from time import sleep
from python.Getir import Getir

from time import time





if __name__ == "__main__":
    getir = Getir(False,50)
    # getir.get_all_getir_products()
    
    
    while True:
        try:
            
            category_list = getir.get_category_list()
            for index,category in enumerate(category_list):
                print(f"{index}-{category.name}")    
            category_index = int(input("Enter category index: "))
            selected_category = category_list[category_index]
            
            sub_category_list = getir.get_sub_categories_with_category(selected_category)
            for index,sub_category in enumerate(sub_category_list):
                print(f"{index}-{sub_category.name}")
        except:
            print("SEÇİM YAPILAMADI")
            exit()
        sub_category_index = int(input("Enter sub category index: "))
        selected_sub_category = sub_category_list[sub_category_index]
        getir.go_sub_category(selected_sub_category)
        getir.get_product_list_web(selected_sub_category)
  
    
    
    # Print category_list and select category, print sub_category_list and select sub_category, print all product of sub_category
    # while True:
    #     category_list = getir.get_category_list()
    #     for index,category in enumerate(category_list):
    #         print(f"{index}-{category.name}")    
    #     category_index = int(input("Enter category index: "))
    #     selected_category = category_list[category_index]
        
    #     sub_category_list = getir.get_sub_categories_with_category(selected_category)
    #     for index,sub_category in enumerate(sub_category_list):
    #         print(f"{index}-{sub_category.name}")
        
    #     sub_category_index = int(input("Enter sub category index: "))
    #     selected_sub_category = sub_category_list[sub_category_index]
        
    #     #get product from sub category
    #     product_list = getir.get_product_list_db(selected_sub_category)
    #     for index, product in enumerate(product_list):
    #         print(f"{index}) {product.name} {product.description} {product.price.price_value}₺")
