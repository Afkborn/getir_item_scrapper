
class Price:
    def __init__(self,
                id : int = None,
                price_value : float = None,
                product_id : int = None,
                time_unix : float = None) -> None:
        self.id = id
        self.price_value = price_value
        self.product_id = product_id
        self.time_unix = time_unix


