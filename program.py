from company import Company

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *

import sqlite3

from employee import Employee
from customer import Customer
from vendor import Vendor
from inventory_item import InventoryItem

class ViewDatabasePopup:
    def __init__(self, master, cursor, table_name):
        self.master = master
        self.cursor = cursor
        self.table_name = table_name

        self.popup = tk.Toplevel(master)
        self.popup.title(f"{self.table_name} Table")

        column_names = self.get_column_names()
        self.tree = ttk.Treeview(self.popup, columns=column_names, show="headings")
        # Create a horizontal scrollbar
        xscrollbar = ttk.Scrollbar(self.popup, orient='horizontal', command=self.tree.xview)
        xscrollbar.grid(row=1, column=0, sticky='ew')

        # Configure Treeview to use the scrollbar for horizontal scrolling
        self.tree.configure(xscrollcommand=xscrollbar.set)

        for name in column_names:
            self.tree.heading(name, text=name)
            self.tree.column(name, width=100)
        self.tree.grid(row=0, column=0, padx=10, pady=10)

        self.populate_table()

    def populate_table(self):
        self.cursor.execute(f"SELECT * FROM {self.table_name}")
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def get_column_names(self):
        self.cursor.execute(f"PRAGMA table_info({self.table_name})")
        columns = self.cursor.fetchall()

        column_names = [column[1] for column in columns]

        # conn.close()

        return column_names
    
class EmployeePaymentPopup:
    def __init__(self, master, cursor, company):
        self.master = master
        self.cursor = cursor
        self.company = company

        # Create a dropdown menu to select the employee
        self.selected_employee = tk.StringVar()
        self.employee_dropdown = ttk.Combobox(master, textvariable=self.selected_employee)
        self.employee_dropdown.pack(pady=10)
        self.populate_employee_dropdown()

        # Create a button to pay the selected employee
        self.pay_button = ttk.Button(master, text="Pay Employee", command=lambda: self.pay_employee(self.selected_employee.get()))
        self.pay_button.pack(pady=10)

    def populate_employee_dropdown(self):
        self.cursor.execute("SELECT FIRST_NAME, LAST_NAME FROM Employees")
        employees = [f"{row[0]} {row[1]}" for row in self.cursor.fetchall()]
        self.employee_dropdown['values'] = employees

    def pay_employee(self, selected_employee):
        # i. Update the balance sheet based on the cash outflow shown on the
        #    employee listing sheet
        # ii. Update the income statement based on the cash outflow shown on
        #     the employee listing sheet
        # iii. Document the history of payroll events
        if selected_employee:
            # Split the selected employee name into first name and last name
            first_name, last_name = selected_employee.split()

            # Query the database to fetch the salary of the selected employee
            self.cursor.execute("SELECT SALARY FROM Employees WHERE FIRST_NAME=? AND LAST_NAME=?", (first_name, last_name))
            salary = self.cursor.fetchone()[0]  # Fetch the first row and the SALARY column value

            self.company.pay_employee(salary)

            print(f"Paying employee: {selected_employee}, Salary: {salary}")
        else:
            tk.messagebox.showwarning("No Employee Selected", "Please select an employee to pay.")

class PurchaseOrderPopup:
    def __init__(self, master, cursor, company):
        self.master = master
        self.cursor = cursor
        self.company = company

        # Check if the inventory database is empty
        self.cursor.execute("SELECT COUNT(*) FROM Inventory")
        count = self.cursor.fetchone()[0]
        
        # Dropdown menu to select an existing inventory item
        self.selected_item = tk.StringVar()
        self.item_dropdown = ttk.Combobox(master, textvariable=self.selected_item)
        self.item_dropdown.pack(pady=10)
        self.populate_item_dropdown()

        # Entry to enter the quantity of items desired
        self.quantity_label = ttk.Label(master, text="Quantity:")
        self.quantity_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(master)
        self.quantity_entry.pack(side=tk.LEFT, padx=5, pady=5)

        # Button to confirm and create the purchase order
        self.create_po_button = ttk.Button(master, text="Create Purchase Order", command=self.create_purchase_order)
        self.create_po_button.pack(pady=10)

    def populate_item_dropdown(self):
        self.cursor.execute("SELECT ITEM_NAME FROM Inventory")
        items = [row[0] for row in self.cursor.fetchall()]
        self.item_dropdown['values'] = items

    def create_purchase_order(self):
        selected_item = self.selected_item.get()
        quantity = self.quantity_entry.get()

        if selected_item and quantity:
            # Add logic to create the purchase order and update databases
            print(f"Creating purchase order for {quantity} units of {selected_item}")
            # Update the balance sheet, inventory, and purchase order history databases
            # self.update_balance_sheet(selected_item, quantity)
            # self.update_inventory(selected_item, quantity)
            # self.update_purchase_order_history(selected_item, quantity)
            self.company.purchase_inventory_item(selected_item, int(quantity))
            messagebox.showinfo("Purchase Order Created", f"Purchase order for {quantity} units of {selected_item} created successfully.")
        else:
            messagebox.showwarning("Incomplete Information", "Please select an item and enter the quantity.")

class InvoicePopup:
    def __init__(self, master, cursor, company):
        self.master = master
        self.cursor = cursor
        self.company = company

        # Dropdown menu to select a customer
        self.selected_customer = tk.StringVar()
        self.customer_dropdown = ttk.Combobox(master, textvariable=self.selected_customer)
        self.customer_dropdown.pack(pady=10)
        self.populate_customer_dropdown()

        # Display current units in stock
        self.units_label = ttk.Label(master, text="Current Units in Stock:")
        self.units_label.pack(pady=5)
        self.display_current_units()

        # Entry to enter the number of units to invoice
        self.units_entry = ttk.Entry(master)
        self.units_entry.pack(pady=5)

        # Button to confirm and create the invoice
        self.create_invoice_button = ttk.Button(master, text="Create Invoice", command=self.create_invoice)
        self.create_invoice_button.pack(pady=10)

    def populate_customer_dropdown(self):
        self.cursor.execute("SELECT COMPANY_NAME FROM Customers")
        customers = [row[0] for row in self.cursor.fetchall()]
        self.customer_dropdown['values'] = customers

    def display_current_units(self):
        # Add logic to fetch and display current units in stock
        # For demonstration purposes, just show a hardcoded value
        self.units_label.config(text=f"Current Units in Stock: {self.company.units_in_stock}")

    def create_invoice(self):
        selected_customer_company = self.selected_customer.get()
        units_to_invoice = self.units_entry.get()

        if selected_customer_company and units_to_invoice:
            # Add logic to create the invoice and update databases
            print(f"Creating invoice for {units_to_invoice} units for customer {selected_customer_company}")
            # Update the balance sheet, income statement, and inventory databases
            self.company.invoice_customer(selected_customer_company, int(units_to_invoice))
            messagebox.showinfo("Invoice Created", f"Invoice for {units_to_invoice} units created successfully for customer {selected_customer_company}.")
        else:
            messagebox.showwarning("Incomplete Information", "Please select a customer and enter the number of units to invoice.")

    def update_balance_sheet(self, units):
        # Add logic to update the balance sheet with receivables from the sale
        self.company.assets.update

    def update_income_statement(self, units):
        # Add logic to update the income statement with sales
        pass

    def update_inventory(self, units):
        # Add logic to update the inventory to reflect the sale of complete units
        pass

class BalanceSheetPopup:
    def __init__(self, master, balance_sheet):
        self.master = master
        self.balance_sheet = balance_sheet

        self.create_assets_table()
        self.create_liabilities_table()

    def create_assets_table(self):
        # Create assets treeview
        self.assets_tree = ttk.Treeview(self.master)
        self.assets_tree.pack(side="left", fill="both", expand=True)

        # Configure assets columns
        self.assets_tree["columns"] = ("Value")
        self.assets_tree.column("#0", width=200, anchor=tk.W)
        self.assets_tree.heading("#0", text="Item", anchor=tk.W)

        self.assets_tree.column("Value", width=200, anchor=tk.W)
        self.assets_tree.heading("Value", text="Value", anchor=tk.W)

        # Add assets section
        assets_node = self.assets_tree.insert("", tk.END, text="Assets", open=True)

        self.add_tree_node(self.assets_tree, assets_node, "Cash", self.balance_sheet.assets.cash)
        self.add_tree_node(self.assets_tree, assets_node, "Accounts Receivable", self.balance_sheet.assets.accounts_recv)
        self.add_tree_node(self.assets_tree, assets_node, "Inventory", self.balance_sheet.assets.inventory)

        total_current_assets = self.balance_sheet.assets.get_total_current_assets()
        self.add_tree_node_bold(self.assets_tree, assets_node, "Total Current Assets", total_current_assets)
        self.add_tree_node(self.assets_tree, assets_node, "Land/Buildings", self.balance_sheet.assets.land_buildings)
        self.add_tree_node(self.assets_tree, assets_node, "Equipment", self.balance_sheet.assets.equipment)
        self.add_tree_node(self.assets_tree, assets_node, "Furniture and Fixtures", self.balance_sheet.assets.furniture_fixtures)

        total_fixed_assets = self.balance_sheet.assets.get_total_fixed_assets()
        self.add_tree_node_bold(self.assets_tree, assets_node, "Total Fixed Assets", total_fixed_assets)
        self.add_tree_node_bold(self.assets_tree, assets_node, "Total Assets", total_current_assets + total_fixed_assets)

    def create_liabilities_table(self):
        # Create liabilities treeview
        self.liabilities_tree = ttk.Treeview(self.master)
        self.liabilities_tree.pack(side="left", fill="both", expand=True)

        # Configure liabilities columns
        self.liabilities_tree["columns"] = ("Value")
        self.liabilities_tree.column("#0", width=200, anchor=tk.W)
        self.liabilities_tree.heading("#0", text="Item", anchor=tk.W)

        self.liabilities_tree.column("Value", width=200, anchor=tk.W)
        self.liabilities_tree.heading("Value", text="Value", anchor=tk.W)

        # Add liabilities section
        liabilities_node = self.liabilities_tree.insert("", tk.END, text="Liabilities & Net Worth", open=True)

        self.add_tree_node(self.liabilities_tree, liabilities_node, "Accounts Payable", self.balance_sheet.liabilities.accounts_payable)
        self.add_tree_node(self.liabilities_tree, liabilities_node, "Notes Payable", self.balance_sheet.liabilities.notes_payable)
        self.add_tree_node(self.liabilities_tree, liabilities_node, "Accruals", self.balance_sheet.liabilities.accruals)

        total_current_liabilities = self.balance_sheet.liabilities.get_total_current_liabilities()
        self.add_tree_node_bold(self.liabilities_tree, liabilities_node, "Total Current Liabilities", total_current_liabilities)
        self.add_tree_node(self.liabilities_tree, liabilities_node, "Mortgage", self.balance_sheet.liabilities.mortgage)

        total_long_term_debt = self.balance_sheet.liabilities.get_total_long_term_debt()
        self.add_tree_node_bold(self.liabilities_tree, liabilities_node, "Total Long Term Debt", total_long_term_debt)
        self.add_tree_node_bold(self.liabilities_tree, liabilities_node, "Total Liabilities", total_current_liabilities + total_long_term_debt)

        self.add_tree_node_bold(self.liabilities_tree, liabilities_node, "Net Worth", self.balance_sheet.net_worth)

    def add_tree_node(self, tree, parent, text, value):
        tree.insert(parent, tk.END, text=text, values=(value,))

    def add_tree_node_bold(self, tree, parent, text, value):
        item = tree.insert(parent, tk.END, text=text, values=(value,))
        tree.tag_configure('bold', font=('Arial', 10, 'bold'))
        tree.item(item, tags=('bold',))

class IncomeStatementPopup:
    def __init__(self, master, income_statement):
        self.master = master
        self.income_statement = income_statement

        # Define bold font
        bold_font = ("TkDefaultFont", 10, "bold")
        section_font = ("TkDefaultFont", 12, "bold")

        # Sales Section
        tk.Label(self.master, text="Sales", font=section_font).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        tk.Label(self.master, text="Sales:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.master, text=f"${self.income_statement.sales.sales}").grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.master, text="Cost of Goods:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.master, text=f"${self.income_statement.sales.cost_of_goods}").grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.master, text="Gross Profit:", font=bold_font).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.master, text=f"${self.income_statement.sales.get_gross_profits()}", font=bold_font).grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Expenses Section
        tk.Label(self.master, text="Expenses", font=section_font).grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        tk.Label(self.master, text="Payroll:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.master, text=f"${self.income_statement.expenses.payroll}").grid(row=5, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.master, text="Payroll Withholding:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.master, text=f"${self.income_statement.expenses.payroll_witholding}").grid(row=6, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.master, text="Bills:").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.master, text=f"${self.income_statement.expenses.bills}").grid(row=7, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.master, text="Annual Expenses:").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.master, text=f"${self.income_statement.expenses.annual_expenses}").grid(row=8, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.master, text="Total Expenses:", font=bold_font).grid(row=9, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.master, text=f"${self.income_statement.expenses.get_total_expenses()}", font=bold_font).grid(row=9, column=1, padx=5, pady=5, sticky="w")

        # Net Section
        tk.Label(self.master, text="Net", font=section_font).grid(row=10, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        tk.Label(self.master, text="Other Income:").grid(row=11, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.master, text=f"${self.income_statement.other_income}").grid(row=11, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.master, text="Operating Income:").grid(row=12, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.master, text=f"${self.income_statement.sales.get_gross_profits() - self.income_statement.expenses.get_total_expenses()}").grid(row=12, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.master, text="Income Taxes:").grid(row=13, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.master, text=f"${self.income_statement.income_taxes}").grid(row=13, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.master, text="Net Income:", font=bold_font).grid(row=14, column=0, padx=5, pady=5, sticky="w")
        tk.Label(self.master, text=f"${self.income_statement.net_income}", font=bold_font).grid(row=14, column=1, padx=5, pady=5, sticky="w")


class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Financial Management System")

        self.company = Company("Best Corp")

        # GUI Components
        self.employee_button = ttk.Button(master, text="Add Employee", command=self.add_employee)
        self.employee_button.pack(pady=10)

        self.view_employee_button = ttk.Button(master, text="View Employees", command=self.view_employees)
        self.view_employee_button.pack(pady=10)

        # Create a button to open the employee payment popup
        self.pay_employee_button = ttk.Button(master, text="Pay An Employee", command=self.open_payment_popup)
        self.pay_employee_button.pack(pady=10)

        self.customer_button = ttk.Button(master, text="Add Customer", command=self.add_customer)
        self.customer_button.pack(pady=10)

        self.view_employee_button = ttk.Button(master, text="View Customers", command=self.view_customers)
        self.view_employee_button.pack(pady=10)

        self.vendor_button = ttk.Button(master, text="Add Vendor", command=self.add_vendor)
        self.vendor_button.pack(pady=10)

        self.view_vendor_button = ttk.Button(master, text="View Vendors", command=self.view_vendors)
        self.view_vendor_button.pack(pady=10)

        self.view_inventory_button = ttk.Button(master, text="View Inventory", command=self.view_inventory)
        self.view_inventory_button.pack(pady=10)

        # Create a button to open the purchase order popup
        self.create_purchase_order_button = ttk.Button(master, text="Create Purchase Order", command=self.open_purchase_order_popup)
        self.create_purchase_order_button.pack(pady=10)

        self.purchase_order_history = ttk.Button(master, text="Purchase Order History", command=self.view_purchase_order)
        self.purchase_order_history.pack(pady=10)
        
        # Create a button to open the invoice popup
        self.create_invoice_button = ttk.Button(master, text="Create Invoice", command=self.open_invoice_popup)
        self.create_invoice_button.pack(pady=10)

        self.invoice_history_button = ttk.Button(master, text="Invoice History", command=self.view_invoice_history)
        self.invoice_history_button.pack(pady=10)

        self.view_balance_sheet_button = ttk.Button(master, text="Show Balance Sheet", command=self.open_balance_sheet_popup)
        self.view_balance_sheet_button.pack(pady=10)

        self.view_income_statement_button = ttk.Button(master, text="Show Income Statement", command=self.open_income_statement_popup)
        self.view_income_statement_button.pack(pady=10)

        self.result_label = ttk.Label(master, text="")
        self.result_label.pack(pady=10)

        # Display data in Listboxes
        # self.employee_listbox = Listbox(master)
        # self.employee_listbox.pack(pady=10)

        # self.customer_listbox = Listbox(master)
        # self.customer_listbox.pack(pady=10)

        # self.inventory_listbox = Listbox(master)
        # self.inventory_listbox.pack(pady=10)

        # Load initial data
        # self.load_data()
    
    def open_balance_sheet_popup(self):
        popup = tk.Toplevel(self.master)
        popup.title("Balance Sheet")
        BalanceSheetPopup(popup, self.company.balance_sheet)

    def open_income_statement_popup(self):
        popup = tk.Toplevel(self.master)
        popup.title("Income Statement Sheet")
        IncomeStatementPopup(popup, self.company.income_statement)

    def open_payment_popup(self):
        popup = tk.Toplevel(self.master)
        popup.title("Pay Employee")
        EmployeePaymentPopup(popup, self.company.cursor, self.company)
    
    def open_purchase_order_popup(self):
        popup = tk.Toplevel(self.master)
        popup.title("Create Purchase Order")
        PurchaseOrderPopup(popup, self.company.cursor, self.company)

    def open_invoice_popup(self):
        popup = tk.Toplevel(self.master)
        popup.title("Create Invoice")
        InvoicePopup(popup, self.company.cursor, self.company)

    def add_employee(self):
        employee_window = tk.Toplevel(self.master)
        employee_window.title("Add Employee")

        attrs = ["First Name",
                 "Last Name",
                 "Address 1",
                 "Address 2",
                 "City",
                 "State",
                 "Zip Code",
                 "SSN",
                 "Withholdings",
                 "Salary per Payroll (in USD)"]
    
        attr_dict = {attr: None for attr in attrs}
        
        for attr in attr_dict.keys():
            tk.Label(employee_window, text=f"{attr}:").pack()
            entry = tk.Entry(employee_window)
            attr_dict[attr] = entry
            entry.pack()

        tk.Button(employee_window, text="Add Employee", command=lambda: self.save_employee(attr_dict)).pack()

    def save_employee(self, attr_dict):
        # Save employee details to database or perform other operations
        employee_data = [entry.get() for entry in attr_dict.values()]
        new_employee = Employee(*employee_data)
        self.company.add_employee(new_employee)
        # self.load_data()
        messagebox.showinfo("Success", f"Employee {new_employee.first_name} {new_employee.last_name} added successfully.")
        
    def view_employees(self):
        ViewDatabasePopup(self.master, self.company.cursor, "Employees")
    
    def view_invoice_history(self):
        ViewDatabasePopup(self.master, self.company.cursor, "InvoiceHistory")
    
    def view_purchase_order(self):
        ViewDatabasePopup(self.master, self.company.cursor, "PurchaseOrderHistory")
    
    def add_customer(self):
        customer_window = tk.Toplevel(self.master)
        customer_window.title("Add Customer")
        
        attrs = ["Company Name",
                 "First Name",
                 "Last Name",
                 "Address 1",
                 "Address 2",
                 "City",
                 "State",
                 "Zip Code"]
        
        # Price Purchased default $100 first
    
        attr_dict = {attr: None for attr in attrs}

        for attr in attr_dict.keys():
            tk.Label(customer_window, text=f"{attr}:").pack()
            entry = tk.Entry(customer_window)
            attr_dict[attr] = entry
            entry.pack()

        tk.Button(customer_window, text="Add Customer", command=lambda: self.save_customer(attr_dict)).pack()

    def save_customer(self, attr_dict):
        # Save customer details to database or perform other operations
        customer_data = [entry.get() for entry in attr_dict.values()]
        new_customer = Customer(*customer_data)
        self.company.add_customer(new_customer)
        # self.load_data()
        messagebox.showinfo("Success", f"Customer added successfully.")
    
    def view_customers(self):
        ViewDatabasePopup(self.master, self.company.cursor, "Customers")

    def add_vendor(self):
        vendor_window = tk.Toplevel(self.master)
        vendor_window.title("Add Vendor")
        
        attrs = ["Company Name",
                 "Item Name",
                 "Price per Unit",
                 "Address 1",
                 "Address 2",
                 "City",
                 "State",
                 "Zip Code"]
    
        attr_dict = {attr: None for attr in attrs}

        for attr in attr_dict.keys():
            tk.Label(vendor_window, text=f"{attr}:").pack()
            entry = tk.Entry(vendor_window)
            attr_dict[attr] = entry
            entry.pack()

        tk.Button(vendor_window, text="Add Vendor", command=lambda: self.save_vendor(attr_dict)).pack()

    def save_vendor(self, attr_dict):
        # Save customer details to database or perform other operations
        vendor_data = [entry.get() for entry in attr_dict.values()]
        new_vendor = Vendor(*vendor_data)
        self.company.add_vendor(new_vendor)
        new_inventory_item = InventoryItem(new_vendor.company_name, new_vendor.item_name, new_vendor.price_per_unit, 0)
        self.company.add_inventory_item(new_inventory_item)
        # self.load_data()
        messagebox.showinfo("Success", f"Vendor added successfully.")

    def view_vendors(self):
        ViewDatabasePopup(self.master, self.company.cursor, "Vendors")

    def view_inventory(self):
        ViewDatabasePopup(self.master, self.company.cursor, "Inventory")

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
