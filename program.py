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
    def __init__(self, master, cursor):
        self.master = master
        self.cursor = cursor

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
        # TODO change balance sheets and stuff: add logic to pay the selected employee
        if selected_employee:
            print(f"Paying employee: {selected_employee}")
        else:
            tk.messagebox.showwarning("No Employee Selected", "Please select an employee to pay.")

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

        self.customer_button = ttk.Button(master, text="Add Customer", command=self.add_customer)
        self.customer_button.pack(pady=10)

        self.view_employee_button = ttk.Button(master, text="View Customers", command=self.view_customers)
        self.view_employee_button.pack(pady=10)

        self.vendor_button = ttk.Button(master, text="Add Vendor", command=self.add_vendor)
        self.vendor_button.pack(pady=10)

        self.view_vendor_button = ttk.Button(master, text="View Vendors", command=self.view_vendors)
        self.view_vendor_button.pack(pady=10)

        # Create a button to open the employee payment popup
        self.pay_employee_button = ttk.Button(master, text="Pay An Employee", command=self.open_payment_popup)
        self.pay_employee_button.pack(pady=10)

        # self.inventory_button = ttk.Button(master, text="Add Inventory Item", command=self.add_inventory_item)
        # self.inventory_button.pack(pady=10)

        self.calculate_button = ttk.Button(master, text="Calculate", command=self.calculate)
        self.calculate_button.pack(pady=10)

        self.result_label = ttk.Label(master, text="")
        self.result_label.pack(pady=10)

        # Display data in Listboxes
        self.employee_listbox = Listbox(master)
        self.employee_listbox.pack(pady=10)

        self.customer_listbox = Listbox(master)
        self.customer_listbox.pack(pady=10)

        self.inventory_listbox = Listbox(master)
        self.inventory_listbox.pack(pady=10)

        # Load initial data
        self.load_data()


    def open_payment_popup(self):
        popup = tk.Toplevel(self.master)
        popup.title("Pay Employee")
        EmployeePaymentPopup(popup, self.company.cursor)


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
        self.load_data()
        messagebox.showinfo("Success", f"Employee {new_employee.first_name} {new_employee.last_name} added successfully.")
        
    def view_employees(self):
        ViewDatabasePopup(self.master, self.company.cursor, "Employees")
    
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
                 "Zip Code",
                 "Price Purchased"]
    
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
        self.load_data()
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
        self.load_data()
        messagebox.showinfo("Success", f"Vendor added successfully.")
    
    def view_vendors(self):
        ViewDatabasePopup(self.master, self.company.cursor, "Vendors")













    def add_inventory_item(self):
        inventory_window = tk.Toplevel(self.master)
        inventory_window.title("Add Inventory Item")

        tk.Label(inventory_window, text="Item Name:").pack()
        item_name_entry = tk.Entry(inventory_window)
        item_name_entry.pack()

        tk.Label(inventory_window, text="Item :").pack()
        item_id_entry = tk.Entry(inventory_window)
        item_id_entry.pack()

        tk.Label(inventory_window, text="Quantity:").pack() # int
        item_quantity_entry = tk.Entry(inventory_window)
        item_quantity_entry.pack()

        tk.Label(inventory_window, text="Unit Price:").pack() # float
        item_unit_price_entry = tk.Entry(inventory_window)
        item_unit_price_entry.pack()

        tk.Button(inventory_window, text="Add Customer", command=lambda: self.save_customer(item_name_entry.get(), item_id_entry.get())).pack()
        
    def save_inventory(self, name, item_id, quantity, unit_price):
        # Save customer details to database or perform other operations
        messagebox.showinfo("Success", f"{quantity} items of {name} with ID {item_id} at ${unit_price} each added successfully.")

    # def add_inventory_item(self):
    #     # name = input("Enter item name: ")
    #     # quantity = int(input("Enter quantity: "))
    #     # unit_price = float(input("Enter unit price: "))
    #     # item = InventoryItem(name, quantity, unit_price)
    #     self.company.add_inventory_item(item)
    #     self.load_data()

    def calculate(self):
        income_statement = self.company.calculate_income_statement()
        balance_sheet = self.company.calculate_balance_sheet()

        result_text = f"Income Statement: {income_statement}\nBalance Sheet: {balance_sheet}"
        self.result_label.config(text=result_text)

    def load_data(self):
        # Clear existing data
        self.employee_listbox.delete(0, tk.END)
        self.customer_listbox.delete(0, tk.END)
        self.inventory_listbox.delete(0, tk.END)

        # Load employee data
        employees = self.company.get_employees()
        for employee in employees:
            self.employee_listbox.insert(tk.END, f"{employee[0]} - {employee[1]}")

        # Load customer data
        customers = self.company.get_customers()
        for customer in customers:
            self.customer_listbox.insert(tk.END, customer[0])

        # Load inventory item data
        inventory_items = self.company.get_inventory_items()
        for item in inventory_items:
            self.inventory_listbox.insert(tk.END, f"{item[0]} - {item[1]} - {item[2]}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
