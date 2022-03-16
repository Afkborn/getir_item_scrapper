from python.model.Price import Price

class Product:
    def __init__(self,
                id : int = None,
                name : str = None,
                paragraph : str = None,
                category_id : int = None,
                sub_category_id : int =None,
                price : Price = None) -> None:
        self.id = id
        self.name = name
        self.paragraph = paragraph
        self.category_id = category_id
        self.sub_category_id = sub_category_id
        self.price = price