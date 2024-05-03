import tkinter as tk
from tkinter import ttk

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
        self.sales = new_sales
        self.net_income = self.calculate_net_income()

    def update_expenses(self, new_expenses):
        self.expenses = new_expenses
        self.net_income = self.calculate_net_income()
    


import tkinter as tk
from tkinter import ttk

class IncomeStatementPopup:
    def __init__(self, master, income_statement):
        self.master = master
        self.income_statement = income_statement

        self.popup = tk.Toplevel(master)
        self.popup.title("Income Statement")

        # Define bold font
        bold_font = ("TkDefaultFont", 10, "bold")
        section_font = ("TkDefaultFont", 12, "bold")

        # Sales Section
        tk.Label(self.popup, text="Sales", font=section_font).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        tk.Label(self.popup, text="Sales:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.popup, text=f"${self.income_statement.sales.sales}").grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.popup, text="Cost of Goods:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.popup, text=f"${self.income_statement.sales.cost_of_goods}").grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.popup, text="Gross Profit:", font=bold_font).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.popup, text=f"${self.income_statement.sales.get_gross_profits()}", font=bold_font).grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Expenses Section
        tk.Label(self.popup, text="Expenses", font=section_font).grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        tk.Label(self.popup, text="Payroll:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.popup, text=f"${self.income_statement.expenses.payroll}").grid(row=5, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.popup, text="Payroll Withholding:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.popup, text=f"${self.income_statement.expenses.payroll_witholding}").grid(row=6, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.popup, text="Bills:").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.popup, text=f"${self.income_statement.expenses.bills}").grid(row=7, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.popup, text="Annual Expenses:").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.popup, text=f"${self.income_statement.expenses.annual_expenses}").grid(row=8, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.popup, text="Total Expenses:", font=bold_font).grid(row=9, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.popup, text=f"${self.income_statement.expenses.get_total_expenses()}", font=bold_font).grid(row=9, column=1, padx=5, pady=5, sticky="w")

        # Net Section
        tk.Label(self.popup, text="Net", font=section_font).grid(row=10, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        tk.Label(self.popup, text="Other Income:").grid(row=11, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.popup, text=f"${self.income_statement.other_income}").grid(row=11, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.popup, text="Operating Income:").grid(row=12, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.popup, text=f"${self.income_statement.sales.get_gross_profits() - self.income_statement.expenses.get_total_expenses()}").grid(row=12, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.popup, text="Income Taxes:").grid(row=13, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.popup, text=f"${self.income_statement.income_taxes}").grid(row=13, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.popup, text="Net Income:", font=bold_font).grid(row=14, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.popup, text=f"${self.income_statement.net_income}", font=bold_font).grid(row=14, column=1, padx=5, pady=5, sticky="w")

if __name__ == "__main__":
    root = tk.Tk()
    
    # Create sample objects for Sales, Expenses, and IncomeStatement
    sales = Sales(50000, 30000)
    expenses = Expenses(20000, 5000, 10000, 15000)
    income_statement = IncomeStatement(sales, expenses, 5000, 10000)
    
    IncomeStatementPopup(root, income_statement)
    
    root.mainloop()
