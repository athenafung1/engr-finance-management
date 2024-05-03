import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class InvoicePopup:
    def __init__(self, master):
        self.master = master
        self.master.title("Create Invoice")
        self.connection = sqlite3.connect("company_database.db")
        self.cursor = self.connection.cursor()

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
        units_in_stock = 100
        self.units_label.config(text=f"Current Units in Stock: {units_in_stock}")

    def create_invoice(self):
        selected_customer = self.selected_customer.get()
        units_to_invoice = self.units_entry.get()

        if selected_customer and units_to_invoice:
            # Add logic to create the invoice and update databases
            print(f"Creating invoice for {units_to_invoice} units for customer {selected_customer}")
            # Update the balance sheet, income statement, and inventory databases
            self.update_balance_sheet(selected_customer, units_to_invoice)
            self.update_income_statement(units_to_invoice)
            self.update_inventory(units_to_invoice)
            messagebox.showinfo("Invoice Created", f"Invoice for {units_to_invoice} units created successfully for customer {selected_customer}.")
        else:
            messagebox.showwarning("Incomplete Information", "Please select a customer and enter the number of units to invoice.")

    def update_balance_sheet(self, customer, units):
        # Add logic to update the balance sheet with receivables from the sale
        pass

    def update_income_statement(self, units):
        # Add logic to update the income statement with sales
        pass

    def update_inventory(self, units):
        # Add logic to update the inventory to reflect the sale of complete units
        pass

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Main GUI")

        # Create a button to open the invoice popup
        self.create_invoice_button = ttk.Button(master, text="Create Invoice", command=self.open_invoice_popup)
        self.create_invoice_button.pack(pady=10)

    def open_invoice_popup(self):
        popup = tk.Toplevel(self.master)
        invoice_popup = InvoicePopup(popup)

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
