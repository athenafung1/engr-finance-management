import copy

class Assets:
    def __init__(self, 
                 cash, 
                 accounts_recv,
                 inventory,
                 land_buildings,
                 equipment,
                 furniture_fixtures):
        self.cash = cash
        self.accounts_recv = accounts_recv
        self.inventory = inventory

        self.land_buildings = land_buildings
        self.equipment = equipment
        self.furniture_fixtures = furniture_fixtures

    def get_total_current_assets(self):
        return self.cash + self.accounts_recv + self.inventory
    
    def get_total_fixed_assets(self):
        return self.land_buildings + self.equipment + self.furniture_fixtures
    
    def get_total_assets(self):
        return self.get_total_current_assets() + self.get_total_fixed_assets()

class Liabilities:
    def __init__(self,
                 accounts_payable,
                 notes_payable,
                 accruals,
                 mortgage):
        self.accounts_payable = accounts_payable
        self.notes_payable = notes_payable
        self.accruals = accruals

        self.mortgage = mortgage

    def get_total_current_liabilities(self):
        return self.accounts_payable + self.notes_payable + self.accruals
    
    def get_total_long_term_debt(self):
        return self.mortgage
    
    def get_total_liabilities(self):
        return self.get_total_current_liabilities() + self.get_total_long_term_debt()

class BalanceSheet:
    def __init__(self, 
                 assets,
                 liabilities):
        self.assets = assets
        self.liabilities = liabilities
        self.net_worth = self.calculate_net_worth()
        
    def calculate_net_worth(self):
        net_worth = self.assets.get_total_assets() - self.liabilities.get_total_liabilities()
        return net_worth
    
    def update_assets(self, new_assets):
        self.assets = copy.deepcopy(new_assets)
        self.net_worth = self.calculate_net_worth()

    def update_liabilities(self, new_liabilities):
        self.liabilities = copy.deepcopy(new_liabilities)
        self.net_worth = self.calculate_net_worth()
    
