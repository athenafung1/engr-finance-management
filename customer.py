class Customer:
    def __init__(self, 
                 company_name, 
                 first_name,
                 last_name,
                 address1,
                 address2,
                 city,
                 state,
                 zipcode,
                 price):
        self.company_name = company_name
        self.first_name = first_name
        self.last_name = last_name
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.price = price