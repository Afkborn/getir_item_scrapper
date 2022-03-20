
class Price:
    def __init__(self,
                id : int = None,
                price_value : float = None,
                product_id : int = None,
                time_unix : float = None,
                has_discount : bool = None,
                discount_price : float = None ) -> None:
        self.id = id
        self.price_value = price_value
        self.product_id = product_id
        self.time_unix = time_unix
        self.has_discount = has_discount
        self.discount_price = discount_price


