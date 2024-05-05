import copy

class Sales:
    def __init__(self, 
                 sales, 
                 cost_of_goods):
        self.sales = sales
        self.cost_of_goods = cost_of_goods

    def get_gross_profits(self):
        return self.sales - self.cost_of_goods

class Expenses:
    def __init__(self,
                 payroll,
                 payroll_witholding,
                 bills,
                 annual_expenses):
        self.payroll = payroll
        self.payroll_witholding = payroll_witholding
        self.bills = bills
        self.annual_expenses = annual_expenses
    def get_total_expenses(self):
        return self.payroll + self.bills + self.annual_expenses
    
class IncomeStatement:
    def __init__(self, 
                 sales,
                 expenses,
                 other_income,
                 income_taxes):
        self.sales = sales
        self.expenses = expenses
        self.other_income = other_income
        self.income_taxes = income_taxes
        self.net_income = self.calculate_net_income()
        
    def calculate_net_income(self):
        net_income = self.sales.get_gross_profits() - self.expenses.get_total_expenses()
        return net_income
    
    def update_sales(self, new_sales):
        self.sales = copy.deepcopy(new_sales)
        self.net_income = self.calculate_net_income()

    def update_expenses(self, new_expenses):
        self.expenses = copy.deepcopy(new_expenses)
        self.net_income = self.calculate_net_income()
    
