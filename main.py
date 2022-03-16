from python.Getir import Getir



if __name__ == "__main__":
    getir = Getir(False,50)
    
    getir.get_getir_category()

    getir_category_list = getir.load_category_list()
    for index,category in enumerate(getir_category_list):
        if index % 5 == 0:
            print(" ")
        elif index == len(getir_category_list):
            print("\n")
        print(f"{index}){category.name}",end="   ")
    selected_category = input("\nSelected Category (example 1): ")
    selected_category = int(selected_category)
    sub_category =  getir.get_getir_sub_category(getir_category_list[selected_category])