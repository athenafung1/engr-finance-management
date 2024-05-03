import tkinter as tk
from tkinter import ttk
from tkinter import *
import sqlite3

from employee import Employee
from customer import Customer
from vendor import Vendor
from inventory_item import InventoryItem


class Company:
    def __init__(self, name, database_path="company_database.db"):
        self.name = name
        self.database_path = database_path
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

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
                           ITEM_NAME TEXT, 
                           UNIT_PRICE REAL,
                           QUANTITY INTEGER, 
                           VALUE REAL)''')

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
        price = float(customer.price) if customer.price else ''
        self.cursor.execute("INSERT INTO Customers (COMPANY_NAME, FIRST_NAME, LAST_NAME, ADDRESS1, ADDRESS2, CITY, STATE, ZIPCODE, PRICE) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                            (customer.company_name,customer.first_name, customer.last_name, customer.address1, customer.address2,
                              customer.city, customer.state, customer.zipcode, price))
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
        self.cursor.execute("INSERT INTO Inventory (ITEM_NAME, UNIT_PRICE, QUANTITY, VALUE) VALUES (?, ?, ?, ?)",
                       (item.item_name, item.unit_price, item.quantity, value))
        self.connection.commit()

    def get_inventory_items(self):
        # cursor = self.connection.cursor()
        self.cursor.execute("SELECT * FROM Inventory")
        return self.cursor.fetchall()

    def calculate_income_statement(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT SUM(salary) FROM employees")
        total_income = cursor.fetchone()[0] or 0  # Handle None if no records found

        cursor.execute("SELECT SUM(quantity * unit_price) FROM inventory")
        total_expenses = cursor.fetchone()[0] or 0  # Handle None if no records found

        net_income = total_income - total_expenses
        return net_income

    def calculate_balance_sheet(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT SUM(quantity * unit_price) FROM inventory")
        total_assets = cursor.fetchone()[0] or 0  # Handle None if no records found

        cursor.execute("SELECT SUM(salary) FROM employees")
        total_liabilities = cursor.fetchone()[0] or 0  # Handle None if no records found

        equity = total_assets - total_liabilities
        return equity