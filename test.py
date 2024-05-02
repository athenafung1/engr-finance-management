# import tkinter as tk
# from tkinter import ttk
# import sqlite3

# class GUI:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Dropdown Menu Example")

#         self.connection = sqlite3.connect("your_database.db")
#         self.cursor = self.connection.cursor()

#         # Create a dropdown menu
#         self.selected_value = tk.StringVar()
#         self.dropdown = ttk.Combobox(master, textvariable=self.selected_value)
#         self.dropdown.pack(pady=10)

#         # Populate the dropdown menu with unique elements from a database column
#         unique_values = self.get_unique_values("your_table", "your_column")
#         self.dropdown['values'] = unique_values

#         # Button to display the selected value
#         self.button = ttk.Button(master, text="Display Selected Value", command=self.display_selected_value)
#         self.button.pack(pady=10)

#     def get_unique_values(self, table_name, column_name):
#         self.cursor.execute(f"SELECT DISTINCT {column_name} FROM {table_name}")
#         unique_values = self.cursor.fetchall()
#         return [value[0] for value in unique_values]

#     def display_selected_value(self):
#         selected_value = self.selected_value.get()
#         if selected_value:
#             tk.messagebox.showinfo("Selected Value", f"The selected value is: {selected_value}")
#         else:
#             tk.messagebox.showwarning("No Value Selected", "Please select a value from the dropdown menu.")

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = GUI(root)
#     root.mainloop()

import tkinter as tk
from tkinter import ttk
import sqlite3

class EmployeePaymentPopup:
    def __init__(self, master):
        self.master = master
        self.master.title("Employee Payment")
        self.connection = sqlite3.connect("company_database.db")
        self.cursor = self.connection.cursor()

        # Create a dropdown menu to select the employee
        self.selected_employee = tk.StringVar()
        self.employee_dropdown = ttk.Combobox(master, textvariable=self.selected_employee)
        self.employee_dropdown.pack(pady=10)
        self.populate_employee_dropdown()

        # Create a button to pay the selected employee
        self.pay_button = ttk.Button(master, text="Pay Employee", command=lambda: self.pay_employee(self.selected_employee.get()))
        self.pay_button.pack(pady=10)

    def populate_employee_dropdown(self):
        self.cursor.execute("SELECT first_name, last_name FROM employees")
        employees = [f"{row[0]} {row[1]}" for row in self.cursor.fetchall()]
        self.employee_dropdown['values'] = employees

    def pay_employee(self, selected_employee):
        if selected_employee:
            # Add logic to pay the selected employee
            print(f"Paying employee: {selected_employee}")
            # You can add further logic here to update the database or perform any other actions
        else:
            tk.messagebox.showwarning("No Employee Selected", "Please select an employee to pay.")

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Main GUI")

        # Create a button to open the employee payment popup
        self.pay_button = ttk.Button(master, text="Pay Employee", command=self.open_payment_popup)
        self.pay_button.pack(pady=10)

    def open_payment_popup(self):
        popup = tk.Toplevel(self.master)
        employee_payment_popup = EmployeePaymentPopup(popup)

if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
