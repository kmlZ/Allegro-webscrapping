class Product:
    def __init__(self, name, price, link, main_link):
        self.name = name
        self.price = price
        self.link = link
        self.main_link = main_link

    def serialize(self):
        return {
            "name" : self.name,
            "price" : self.price,
            "link" : self.link,
            "main_link" : self.main_link

        }
        
    def from_json(self, json_):
        self.name = json_["name"]
        self.price = json_["price"]
        self.link = json_["link"]