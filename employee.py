class Employee:
    def __init__(self, 
                 first_name,
                 last_name,
                 address1,
                 address2,
                 city,
                 state,
                 zipcode,
                 ssn,
                 withholdings,
                 salary):
        self.first_name = first_name
        self.last_name = last_name
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.ssn = ssn
        self.withholdings = withholdings
        self.salary = salary