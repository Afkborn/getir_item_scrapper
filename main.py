from time import sleep
from python.Getir import Getir

from time import time


menu = """
1) Get all sub categories and categories from website
2) Get product by sub category
3) Get product by category
4) Exit
"""


if __name__ == "__main__":
    getir = Getir(False,50)
    # getir.get_all_getir_products()
    dongu_kontrol = True
    while dongu_kontrol:
        print(menu)
        selection = int(input("Selection: "))
        if selection == 1:
            # get all sub categories and categories
            getir.get_getir_category_with_sub_category()
        elif selection == 2:
            # get product by sub category
            pass
        elif selection == 3:
            # get product by category
            pass
        elif selection == 4:
            dongu_kontrol = False
        else:
            print("Invalid selection")
        
        
        
    
    # while True:
    #     try:
            
    #         category_list = getir.get_category_list()
    #         for index,category in enumerate(category_list):
    #             print(f"{index}-{category.name}")    
    #         category_index = int(input("Enter category index: "))
    #         selected_category = category_list[category_index]
            
    #         sub_category_list = getir.get_sub_categories_with_category(selected_category)
    #         for index,sub_category in enumerate(sub_category_list):
    #             print(f"{index}-{sub_category.name}")
    #     except:
    #         print("SEÇİM YAPILAMADI")
    #         exit()
    #     sub_category_index = int(input("Enter sub category index: "))
    #     selected_sub_category = sub_category_list[sub_category_index]
    #     getir.go_sub_category(selected_sub_category)
    #     getir.get_product_list_web(selected_sub_category)
  
    
    
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
