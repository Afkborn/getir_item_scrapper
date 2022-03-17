from python.Getir import Getir



if __name__ == "__main__":
    getir = Getir(False,50)

    #print category list

    # getir.get_getir_category_with_sub_category()
    
    # while True:

    #     category_list = getir.get_category_list()
    #     for index,category in enumerate(category_list):
    #         print(f"{index}-{category.name}")
    #     #input category index
    #     category_index = int(input("Enter category index: "))
    #     selected_category = category_list[category_index]
        
    #     #print sub category list
    #     sub_category_list = getir.get_sub_category_with_category(selected_category)
    #     for index,sub_category in enumerate(sub_category_list):
    #         print(f"{index}-{sub_category.name}")
    #     #input sub category index
    #     sub_category_index = int(input("Enter sub category index: "))
    #     selected_sub_category = sub_category_list[sub_category_index]

    #     getir.go_sub_category(selected_sub_category)

    #     getir.get_product_list_with_sub_category(selected_sub_category)

    category_list = getir.get_category_list()
    myList = [15,16,17,18]
    for i in myList:
        sub_category_list = getir.get_sub_category_with_category(category_list[i])
        for sub_category in sub_category_list:
            if sub_category.name == "İlginizi Çekebilecekler":
                continue
            else:
                getir.go_sub_category(sub_category)
                getir.get_product_list_with_sub_category(sub_category)
