from typing import List
from python.model.SubCategory import SubCategory

class Category:
    sub_category_list = []
    def __init__(self, id = None, name = None, description = None) -> None:
        self.id = id
        self.name = name
        self.description = description

    def __str__(self) -> str:
        return f"({self.id},{self.name},{self.description})"
    
    def add_sub_category(self,sub_category : SubCategory) -> None:
        self.sub_category_list.append(sub_category)
    def get_sub_categories(self) -> List[SubCategory]:
        return self.sub_category_list
    def set_sub_categories(self,sub_category_list : List[SubCategory]) -> None:
        self.sub_category_list = sub_category_list



    