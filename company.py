import tkinter as tk
from tkinter import ttk
from tkinter import *
import sqlite3

from employee import Employee
from customer import Customer
from vendor import Vendor
from inventory_item import InventoryItem
from balance_sheet import BalanceSheet, Assets, Liabilities
from income_statement import IncomeStatement, Sales, Expenses

import datetime

class Company:
    def __init__(self, name, database_path="company_database.db"):
        self.name = name
        self.database_path = database_path
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

        self.cost_of_items_sold = 100
        self.units_in_stock = 500 # TODO update based on inventory

        self.assets = Assets(200000, 0, 10000000, 0, 0, 0)
        self.liabilities = Liabilities(0, 0, 0, 0)
        self.balance_sheet = BalanceSheet(self.assets, self.liabilities)

        self.sales = Sales(50000, 100)
        self.expenses = Expenses(20000, 0, 10000, 15000)
        self.other_income = 0
        self.income_taxes = 0
        self.income_statement = IncomeStatement(self.sales, self.expenses, self.other_income, self.income_taxes)

    def create_tables(self):
        # Create Employees Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Employees
                            (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                            FIRST_NAME TEXT,
                            LAST_NAME TEXT, 
                            ADDRESS1 TEXT,
                            ADDRESS2 TEXT,
                            CITY TEXT,
                            STATE TEXT,
                            ZIPCODE TEXT,
                            SSN TEXT,
                            WITHHOLDINGS REAL,
                            SALARY REAL)''')

        # Create Customers Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Customers
                           (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            COMPANY_NAME TEXT,
                            FIRST_NAME TEXT,
                            LAST_NAME TEXT, 
                            ADDRESS1 TEXT,
                            ADDRESS2 TEXT,
                            CITY TEXT,
                            STATE TEXT,
                            ZIPCODE TEXT,
                            PRICE REAL)''')
        
        # Create Vendors Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Vendors
                           (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            COMPANY_NAME TEXT,
                            ITEM_NAME TEXT,
                            PRICE_PER_UNIT TEXT, 
                            ADDRESS1 TEXT,
                            ADDRESS2 TEXT,
                            CITY TEXT,
                            STATE TEXT,
                            ZIPCODE TEXT)''')

        # Create Inventory Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Inventory
                          (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                           SUPPLIER TEXT,
                           ITEM_NAME TEXT, 
                           UNIT_PRICE REAL,
                           QUANTITY INTEGER, 
                           VALUE REAL)''')
        
    
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS InvoiceHistory (
                                InvoiceNumber INTEGER PRIMARY KEY AUTOINCREMENT,
                                Date TEXT,
                                Customer TEXT,
                                Quantity INTEGER,
                                PricePerPart REAL,
                                Total REAL)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS PurchaseOrderHistory (
                                PurchaseOrderNumber INTEGER PRIMARY KEY AUTOINCREMENT,
                                Date TEXT,
                                Supplier TEXT,
                                ItemName TEXT,
                                Quantity INTEGER,
                                UnitPrice REAL,
                                Total REAL)''')
        self.connection.commit()
    
    def get_database(self, database_name):
        self.cursor.execute(f"SELECT * FROM {database_name}")
        return self.cursor.fetchall()

    def add_employee(self, employee):
        withholdings = float(employee.withholdings) if employee.withholdings else ''
        salary = float(employee.salary) if employee.salary else ''
        self.cursor.execute("INSERT INTO Employees (FIRST_NAME, LAST_NAME, ADDRESS1, ADDRESS2, CITY, STATE, ZIPCODE, SSN, WITHHOLDINGS, SALARY) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                             (employee.first_name, employee.last_name, employee.address1, employee.address2,
                              employee.city, employee.state, employee.zipcode, employee.ssn, 
                              withholdings, salary))
        self.connection.commit()
    
    def get_employees(self):
        # cursor = self.connection.cursor()
        self.cursor.execute("SELECT * FROM Employees")
        return self.cursor.fetchall()
    
        # return get_database("Employees")

    def add_customer(self, customer):
        # price = float(customer.price) if customer.price else ''
        default_initial_price = 100
        self.cursor.execute("INSERT INTO Customers (COMPANY_NAME, FIRST_NAME, LAST_NAME, ADDRESS1, ADDRESS2, CITY, STATE, ZIPCODE, PRICE) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                            (customer.company_name,customer.first_name, customer.last_name, customer.address1, customer.address2,
                              customer.city, customer.state, customer.zipcode, default_initial_price))
        self.connection.commit()
    
    def get_customers(self):
        self.cursor.execute("SELECT * FROM Customers")
        return self.cursor.fetchall()
    
        # return get_database("Customers")

    def add_vendor(self, vendor):
        self.cursor.execute("INSERT INTO Vendors (COMPANY_NAME, ITEM_NAME, PRICE_PER_UNIT, ADDRESS1, ADDRESS2, CITY, STATE, ZIPCODE) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                            (vendor.company_name,vendor.item_name, vendor.price_per_unit, vendor.address1, vendor.address2,
                              vendor.city, vendor.state, vendor.zipcode))
        self.connection.commit()
    
    def get_vendors(self):
        self.cursor.execute("SELECT * FROM Vendors")
        return self.cursor.fetchall()

    def populate_employee_dropdown(self):
        self.cursor.execute("SELECT FIRST_NAME, LAST_NAME FROM Employees")
        employees = [f"{row[0]} {row[1]}" for row in self.cursor.fetchall()]
        return employees

    def add_inventory_item(self, item):
        # cursor = self.connection.cursor()
        value = float(item.unit_price) * float(item.quantity)
        self.cursor.execute("INSERT INTO Inventory (SUPPLIER, ITEM_NAME, UNIT_PRICE, QUANTITY, VALUE) VALUES (?, ?, ?, ?, ?)",
                       (item.supplier, item.item_name, item.unit_price, item.quantity, value))
        self.connection.commit()

    def get_inventory_items(self):
        # cursor = self.connection.cursor()
        self.cursor.execute("SELECT * FROM Inventory")
        return self.cursor.fetchall()

    def pay_employee(self, salary):
        current_assets = self.assets
        new_assets = Assets(current_assets.cash - salary, 
                 current_assets.accounts_recv,
                 current_assets.inventory,
                 current_assets.land_buildings,
                 current_assets.equipment,
                 current_assets.furniture_fixtures)
        self.balance_sheet.update_assets(new_assets)

        current_expense = self.expenses
        new_expenses = Expenses(current_expense.payroll + salary, 
                 current_expense.payroll_witholding,
                 current_expense.bills,
                 current_expense.annual_expenses)
        self.income_statement.update_expenses(new_expenses)

    def invoice_customer(self, customer_company_name, num_purchased):
        amount_to_invoice = num_purchased * self.cost_of_items_sold
        current_assets = self.assets
        new_assets = Assets(current_assets.cash, 
                 current_assets.accounts_recv + amount_to_invoice,
                 current_assets.inventory,
                 current_assets.land_buildings,
                 current_assets.equipment,
                 current_assets.furniture_fixtures)
        self.balance_sheet.update_assets(new_assets)

        current_sales = self.sales
        new_sales = Sales(current_sales.sales + amount_to_invoice,
                          current_sales.cost_of_goods) 
        self.income_statement.update_sales(new_sales)

        self.units_in_stock -= num_purchased

        # Update the PRICE field in the Customers table for the selected customer
        self.cursor.execute("UPDATE Customers SET PRICE = PRICE + ? WHERE COMPANY_NAME=?", (amount_to_invoice, customer_company_name))
        # Commit the transaction to save the changes
        self.connection.commit()

        print(f"Price for customer {customer_company_name} incremented by {amount_to_invoice}.")

        self.cursor.execute("INSERT INTO InvoiceHistory (Date, Customer, Quantity, PricePerPart, Total) VALUES (?, ?, ?, ?, ?)", 
                            (self.get_date(),customer_company_name, num_purchased, self.cost_of_items_sold, amount_to_invoice))
        self.connection.commit()

    def purchase_inventory_item(self, selected_item, quantity):
        # Query the database to fetch the unit price of the selected item
        self.cursor.execute("SELECT UNIT_PRICE FROM Inventory WHERE ITEM_NAME=?", (selected_item,))
        unit_price = self.cursor.fetchone()[0]  # Fetch the first row and the UNIT_PRICE column value

        total_purchase_price = quantity * unit_price

        current_assets = self.assets
        new_assets = Assets(current_assets.cash, 
                 current_assets.accounts_recv,
                 current_assets.inventory + total_purchase_price,
                 current_assets.land_buildings,
                 current_assets.equipment,
                 current_assets.furniture_fixtures)
        self.balance_sheet.update_assets(new_assets)

        current_liabilities = self.liabilities
        new_liability = Liabilities(current_liabilities.accounts_payable + total_purchase_price,
                                    current_liabilities.notes_payable,
                                    current_liabilities.accruals,
                                    current_liabilities.mortgage)
        self.balance_sheet.update_liabilities(new_liability)

        # Update the PRICE field in the Customers table for the selected customer
        self.cursor.execute("UPDATE Inventory SET QUANTITY = QUANTITY + ?, VALUE = VALUE + ? WHERE ITEM_NAME=?", (quantity, total_purchase_price, selected_item))
        # Commit the transaction to save the changes
        self.connection.commit()

        # Query the database to fetch the company name associated with the given item name
        self.cursor.execute("SELECT SUPPLIER FROM Inventory WHERE ITEM_NAME=?", (selected_item,))
        supplier = self.cursor.fetchone()[0]  # Fetch the first row and the COMPANY_NAME column value

        self.cursor.execute("INSERT INTO PurchaseOrderHistory (Date, Supplier, Quantity, UnitPrice, Total) VALUES (?, ?, ?, ?, ?)", 
                            (self.get_date(), supplier, quantity, unit_price, total_purchase_price))
        self.connection.commit()

    def get_date(self):
        current_date = datetime.date.today()
        current_date = current_date.strftime("%Y-%m-%d")
        return current_date