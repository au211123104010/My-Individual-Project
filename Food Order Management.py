import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="leelaviji",
    database="food_order_system"
)

if con.is_connected():
    print("MySQL Connected Successfully")


root = tk.Tk()
root.title("Food Order Management and Sales Analytics System")
root.geometry("1200x700")
root.configure(bg="#eaf2f8")

login_window = tk.Toplevel(root)
login_window.title("Login")
login_window.geometry("400x300")
login_window.resizable(False, False)

tk.Label(
    login_window,
    text="Food Order Management System",
    font=("Arial", 18, "bold")
).pack(pady=25)

tk.Label(
    login_window,
    text="Username",
    font=("Arial", 12)
).pack()

username_entry = tk.Entry(
    login_window,
    width=30
)
username_entry.pack(pady=5)

tk.Label(
    login_window,
    text="Password",
    font=("Arial", 12)
).pack()

password_entry = tk.Entry(
    login_window,
    width=30,
    show="*"
)
password_entry.pack(pady=5)

sidebar = tk.Frame(
    root,
    bg="#16324F",
    width=220
)
sidebar.pack(
    side="left",
    fill="y"
)
sidebar.pack_propagate(False)

content_frame = tk.Frame(
    root,
    bg="#eaf2f8"
)
content_frame.pack(
    side="left",
    fill="both",
    expand=True
)


def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()


def set_active(button):
    buttons = [
        dashboard_btn,
        customer_btn,
        food_btn,
        order_btn,
        sales_btn
    ]

    for btn in buttons:
        btn.configure(bg="#16324F")

    button.configure(bg="#285A7A")


def login():
    username = username_entry.get()
    password = password_entry.get()

    cursor = con.cursor()

    query = """
    SELECT * FROM admin_users
    WHERE username = %s AND password = %s
    """

    cursor.execute(
        query,
        (username, password)
    )

    result = cursor.fetchone()

    cursor.close()

    if result:
        login_window.withdraw()
        root.deiconify()
        show_dashboard()
    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid Username or Password"
        )


def logout():
    root.withdraw()
    login_window.deiconify()


def refresh_dashboard():
    show_dashboard()


def customer_window():
    clear_content()
    set_active(customer_btn)

    customer = content_frame
    customer.configure(bg="#eaf2f8")

    title = tk.Label(
        customer,
        text="Customer Management",
        font=("Arial", 26, "bold"),
        bg="#eaf2f8"
    )
    title.pack(pady=(20, 15))

    form_frame = tk.Frame(
        customer,
        bg="#eaf2f8"
    )
    form_frame.pack(
        anchor="w",
        padx=55,
        pady=5
    )

    tk.Label(
        form_frame,
        text="Customer Name",
        font=("Arial", 12, "bold"),
        bg="#eaf2f8"
    ).grid(
        row=0,
        column=0,
        padx=(0, 15),
        pady=7,
        sticky="w"
    )

    name_entry = tk.Entry(
        form_frame,
        width=35,
        font=("Arial", 12)
    )
    name_entry.grid(
        row=0,
        column=1,
        pady=7
    )

    tk.Label(
        form_frame,
        text="Phone",
        font=("Arial", 12, "bold"),
        bg="#eaf2f8"
    ).grid(
        row=1,
        column=0,
        padx=(0, 15),
        pady=7,
        sticky="w"
    )

    phone_entry = tk.Entry(
        form_frame,
        width=35,
        font=("Arial", 12)
    )
    phone_entry.grid(
        row=1,
        column=1,
        pady=7
    )

    tk.Label(
        form_frame,
        text="Email",
        font=("Arial", 12, "bold"),
        bg="#eaf2f8"
    ).grid(
        row=2,
        column=0,
        padx=(0, 15),
        pady=7,
        sticky="w"
    )

    email_entry = tk.Entry(
        form_frame,
        width=35,
        font=("Arial", 12)
    )
    email_entry.grid(
        row=2,
        column=1,
        pady=7
    )

    tk.Label(
        form_frame,
        text="Address",
        font=("Arial", 12, "bold"),
        bg="#eaf2f8"
    ).grid(
        row=3,
        column=0,
        padx=(0, 15),
        pady=7,
        sticky="w"
    )

    address_entry = tk.Entry(
        form_frame,
        width=35,
        font=("Arial", 12)
    )
    address_entry.grid(
        row=3,
        column=1,
        pady=7
    )

    button_frame = tk.Frame(
        customer,
        bg="#eaf2f8"
    )
    button_frame.place(
        x=600,
        y=120
    )

    table_frame = tk.Frame(
        customer,
        bg="#eaf2f8"
    )
    table_frame.pack(
        fill="both",
        expand=True,
        padx=45,
        pady=(20, 25)
    )

    style = ttk.Style()

    style.configure(
        "Customer.Treeview",
        rowheight=32,
        font=("Arial", 10),
        borderwidth=1,
        relief="solid"
    )

    style.configure(
        "Customer.Treeview.Heading",
        font=("Arial", 11, "bold")
    )

    columns = (
        "ID",
        "Customer Name",
        "Phone",
        "Email",
        "Address"
    )

    customer_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        style="Customer.Treeview"
    )

    for column in columns:
        customer_table.heading(
            column,
            text=column
        )

    customer_table.column(
        "ID",
        width=70,
        anchor="center"
    )

    customer_table.column(
        "Customer Name",
        width=220,
        anchor="center"
    )

    customer_table.column(
        "Phone",
        width=180,
        anchor="center"
    )

    customer_table.column(
        "Email",
        width=280,
        anchor="center"
    )

    customer_table.column(
        "Address",
        width=400,
        anchor="center"
    )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=customer_table.yview
    )

    customer_table.configure(
        yscrollcommand=scrollbar.set
    )

    customer_table.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    def load_customers():
        for item in customer_table.get_children():
            customer_table.delete(item)

        cursor = con.cursor()

        cursor.execute("""
        SELECT
            customer_id,
            customer_name,
            phone,
            email,
            address
        FROM customers
        ORDER BY customer_id
        """)

        rows = cursor.fetchall()

        for row in rows:
            customer_table.insert(
                "",
                tk.END,
                values=row
            )

        cursor.close()

    def add_customer():
        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()
        address = address_entry.get().strip()

        if name == "":
            messagebox.showwarning(
                "Warning",
                "Enter customer name"
            )
            return

        cursor = con.cursor()

        cursor.execute(
            """
            INSERT INTO customers
            (customer_name, phone, email, address)
            VALUES (%s, %s, %s, %s)
            """,
            (
                name,
                phone,
                email,
                address
            )
        )

        con.commit()
        cursor.close()

        load_customers()

        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)

        messagebox.showinfo(
            "Success",
            "Customer added successfully"
        )

    def edit_customer():
        selected = customer_table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a customer"
            )
            return

        customer_id = customer_table.item(
            selected[0],
            "values"
        )[0]

        cursor = con.cursor()

        cursor.execute(
            """
            UPDATE customers
            SET customer_name=%s,
                phone=%s,
                email=%s,
                address=%s
            WHERE customer_id=%s
            """,
            (
                name_entry.get().strip(),
                phone_entry.get().strip(),
                email_entry.get().strip(),
                address_entry.get().strip(),
                customer_id
            )
        )

        con.commit()
        cursor.close()

        load_customers()

        messagebox.showinfo(
            "Success",
            "Customer updated successfully"
        )

    def delete_customer():
        selected = customer_table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a customer"
            )
            return

        customer_id = customer_table.item(
            selected[0],
            "values"
        )[0]

        confirm = messagebox.askyesno(
            "Delete Customer",
            "Are you sure you want to delete?"
        )

        if confirm:
            cursor = con.cursor()

            cursor.execute(
                "DELETE FROM customers WHERE customer_id=%s",
                (customer_id,)
            )

            con.commit()
            cursor.close()

            load_customers()

            messagebox.showinfo(
                "Success",
                "Customer deleted successfully"
            )

    def select_customer(event):
        selected = customer_table.selection()

        if not selected:
            return

        values = customer_table.item(
            selected[0],
            "values"
        )

        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)

        name_entry.insert(0, values[1])
        phone_entry.insert(0, values[2])
        email_entry.insert(0, values[3])
        address_entry.insert(0, values[4])

    tk.Button(
        button_frame,
        text="Add",
        command=add_customer,
        bg="#16324F",
        fg="white",
        font=("Arial", 11, "bold"),
        width=12,
        height=2
    ).pack(side="left", padx=7)

    tk.Button(
        button_frame,
        text="Edit",
        command=edit_customer,
        bg="#2563eb",
        fg="white",
        font=("Arial", 11, "bold"),
        width=12,
        height=2
    ).pack(side="left", padx=7)

    tk.Button(
        button_frame,
        text="Delete",
        command=delete_customer,
        bg="#dc2626",
        fg="white",
        font=("Arial", 11, "bold"),
        width=12,
        height=2
    ).pack(side="left", padx=7)

    tk.Button(
        button_frame,
        text="Exit",
        command=show_dashboard,
        bg="#374151",
        fg="white",
        font=("Arial", 11, "bold"),
        width=12,
        height=2
    ).pack(side="left", padx=7)

    customer_table.bind(
        "<<TreeviewSelect>>",
        select_customer
    )

    load_customers()


def food_window():
    clear_content()
    set_active(food_btn)

    food = content_frame

    title = tk.Label(
        food,
        text="Food Item Management",
        font=("Arial", 26, "bold"),
        bg="#eaf2f8"
    )
    title.pack(pady=(20, 15))

    form_frame = tk.Frame(
        food,
        bg="#eaf2f8"
    )
    form_frame.pack(
        anchor="w",
        padx=60
    )

    labels = [
        "Food Name",
        "Category",
        "Price",
        "Availability"
    ]

    entries = []

    for i, label in enumerate(labels):
        tk.Label(
            form_frame,
            text=label,
            font=("Arial", 12, "bold"),
            bg="#eaf2f8"
        ).grid(
            row=i,
            column=0,
            padx=(0, 20),
            pady=8,
            sticky="w"
        )

        entry = tk.Entry(
            form_frame,
            width=35,
            font=("Arial", 12)
        )

        entry.grid(
            row=i,
            column=1,
            pady=8
        )

        entries.append(entry)

    food_name_entry = entries[0]
    category_entry = entries[1]
    price_entry = entries[2]
    availability_entry = entries[3]

    availability_entry.insert(
        0,
        "Available"
    )

    button_frame = tk.Frame(
        food,
        bg="#eaf2f8"
    )
    button_frame.place(
        x=600,
        y=115
    )

    table_frame = tk.Frame(
        food,
        bg="#eaf2f8"
    )
    table_frame.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=(20, 25)
    )

    style = ttk.Style()

    style.configure(
        "Food.Treeview",
        rowheight=32,
        font=("Arial", 10)
    )

    style.configure(
        "Food.Treeview.Heading",
        font=("Arial", 11, "bold")
    )

    columns = (
        "ID",
        "Food Name",
        "Category",
        "Price",
        "Availability"
    )

    food_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        style="Food.Treeview"
    )

    for column in columns:
        food_table.heading(
            column,
            text=column
        )

    food_table.column(
        "ID",
        width=80,
        anchor="center"
    )

    food_table.column(
        "Food Name",
        width=300,
        anchor="center"
    )

    food_table.column(
        "Category",
        width=250,
        anchor="center"
    )

    food_table.column(
        "Price",
        width=180,
        anchor="center"
    )

    food_table.column(
        "Availability",
        width=250,
        anchor="center"
    )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=food_table.yview
    )

    food_table.configure(
        yscrollcommand=scrollbar.set
    )

    food_table.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    def load_foods():
        for item in food_table.get_children():
            food_table.delete(item)

        cursor = con.cursor()

        cursor.execute("""
        SELECT
            food_id,
            food_name,
            category,
            price,
            availability
        FROM food_items
        ORDER BY food_id
        """)

        rows = cursor.fetchall()

        for row in rows:
            food_table.insert(
                "",
                tk.END,
                values=row
            )

        cursor.close()

    def add_food():
        food_name = food_name_entry.get().strip()
        category = category_entry.get().strip()
        price = price_entry.get().strip()
        availability = availability_entry.get().strip()

        if food_name == "" or category == "" or price == "":
            messagebox.showwarning(
                "Warning",
                "Food Name, Category and Price are required"
            )
            return

        try:
            price = float(price)
        except ValueError:
            messagebox.showwarning(
                "Warning",
                "Enter a valid price"
            )
            return

        cursor = con.cursor()

        cursor.execute(
            """
            INSERT INTO food_items
            (food_name, category, price, availability)
            VALUES (%s, %s, %s, %s)
            """,
            (
                food_name,
                category,
                price,
                availability
            )
        )

        con.commit()
        cursor.close()

        load_foods()

        food_name_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)

        messagebox.showinfo(
            "Success",
            "Food Added Successfully"
        )

    def edit_food():
        selected = food_table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a food item"
            )
            return

        food_id = food_table.item(
            selected[0],
            "values"
        )[0]

        try:
            price = float(
                price_entry.get().strip()
            )
        except ValueError:
            messagebox.showwarning(
                "Warning",
                "Enter a valid price"
            )
            return

        cursor = con.cursor()

        cursor.execute(
            """
            UPDATE food_items
            SET food_name=%s,
                category=%s,
                price=%s,
                availability=%s
            WHERE food_id=%s
            """,
            (
                food_name_entry.get().strip(),
                category_entry.get().strip(),
                price,
                availability_entry.get().strip(),
                food_id
            )
        )

        con.commit()
        cursor.close()

        load_foods()

        messagebox.showinfo(
            "Success",
            "Food Updated Successfully"
        )

    def delete_food():
        selected = food_table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a food item"
            )
            return

        food_id = food_table.item(
            selected[0],
            "values"
        )[0]

        if messagebox.askyesno(
            "Delete Food",
            "Are you sure you want to delete?"
        ):
            cursor = con.cursor()

            cursor.execute(
                "DELETE FROM food_items WHERE food_id=%s",
                (food_id,)
            )

            con.commit()
            cursor.close()

            load_foods()

            messagebox.showinfo(
                "Success",
                "Food Deleted Successfully"
            )

    def select_food(event):
        selected = food_table.selection()

        if not selected:
            return

        values = food_table.item(
            selected[0],
            "values"
        )

        food_name_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        availability_entry.delete(0, tk.END)

        food_name_entry.insert(0, values[1])
        category_entry.insert(0, values[2])
        price_entry.insert(0, values[3])
        availability_entry.insert(0, values[4])

    tk.Button(
        button_frame,
        text="Add",
        command=add_food,
        bg="#16324F",
        fg="white",
        font=("Arial", 11, "bold"),
        width=12,
        height=2
    ).pack(side="left", padx=6)

    tk.Button(
        button_frame,
        text="Edit",
        command=edit_food,
        bg="#2563eb",
        fg="white",
        font=("Arial", 11, "bold"),
        width=12,
        height=2
    ).pack(side="left", padx=6)

    tk.Button(
        button_frame,
        text="Delete",
        command=delete_food,
        bg="#dc2626",
        fg="white",
        font=("Arial", 11, "bold"),
        width=12,
        height=2
    ).pack(side="left", padx=6)

    tk.Button(
        button_frame,
        text="Exit",
        command=show_dashboard,
        bg="#374151",
        fg="white",
        font=("Arial", 11, "bold"),
        width=12,
        height=2
    ).pack(side="left", padx=6)

    food_table.bind(
        "<<TreeviewSelect>>",
        select_food
    )

    load_foods()


def order_window():
    clear_content()
    set_active(order_btn)

    order = content_frame

    title = tk.Label(
        order,
        text="Order Management",
        font=("Arial", 26, "bold"),
        bg="#eaf2f8"
    )
    title.pack(pady=(20, 15))

    form_frame = tk.Frame(
        order,
        bg="#eaf2f8"
    )
    form_frame.pack(
        anchor="w",
        padx=70
    )

    tk.Label(
        form_frame,
        text="Customer Name",
        font=("Arial", 12, "bold"),
        bg="#eaf2f8"
    ).grid(
        row=0,
        column=0,
        padx=(0, 20),
        pady=8
    )

    customer_combo = ttk.Combobox(
        form_frame,
        width=32,
        font=("Arial", 12),
        state="readonly"
    )
    customer_combo.grid(
        row=0,
        column=1
    )

    tk.Label(
        form_frame,
        text="Food Item",
        font=("Arial", 12, "bold"),
        bg="#eaf2f8"
    ).grid(
        row=1,
        column=0,
        padx=(0, 20),
        pady=8
    )

    food_combo = ttk.Combobox(
        form_frame,
        width=32,
        font=("Arial", 12),
        state="readonly"
    )
    food_combo.grid(
        row=1,
        column=1
    )

    tk.Label(
        form_frame,
        text="Quantity",
        font=("Arial", 12, "bold"),
        bg="#eaf2f8"
    ).grid(
        row=2,
        column=0,
        padx=(0, 20),
        pady=8
    )

    quantity_entry = tk.Entry(
        form_frame,
        width=35,
        font=("Arial", 12)
    )
    quantity_entry.grid(
        row=2,
        column=1
    )

    tk.Label(
        form_frame,
        text="Total Amount",
        font=("Arial", 12, "bold"),
        bg="#eaf2f8"
    ).grid(
        row=3,
        column=0,
        padx=(0, 20),
        pady=8
    )

    total_label = tk.Label(
        form_frame,
        text="₹ 0",
        font=("Arial", 14, "bold"),
        bg="#eaf2f8"
    )
    total_label.grid(
        row=3,
        column=1,
        sticky="w"
    )

    button_frame = tk.Frame(
        order,
        bg="#eaf2f8"
    )
    button_frame.place(
        x=600,
        y=115
    )

    table_title = tk.Label(
        order,
        text="Order Details",
        font=("Arial", 18, "bold"),
        bg="#eaf2f8"
    )
    table_title.pack(
        pady=(25, 8)
    )

    table_frame = tk.Frame(
        order,
        bg="#eaf2f8"
    )
    table_frame.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=(5, 25)
    )

    columns = (
        "Order ID",
        "Customer",
        "Food Item",
        "Quantity",
        "Price",
        "Total"
    )

    order_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for column in columns:
        order_table.heading(
            column,
            text=column
        )

    widths = {
        "Order ID": 100,
        "Customer": 220,
        "Food Item": 250,
        "Quantity": 120,
        "Price": 150,
        "Total": 160
    }

    for column in columns:
        order_table.column(
            column,
            width=widths[column],
            anchor="center"
        )

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=order_table.yview
    )

    order_table.configure(
        yscrollcommand=scrollbar.set
    )

    order_table.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    def load_customers():
        cursor = con.cursor()

        cursor.execute("""
        SELECT customer_id, customer_name
        FROM customers
        ORDER BY customer_name
        """)

        rows = cursor.fetchall()

        cursor.close()

        customer_combo["values"] = [
            f"{row[0]} - {row[1]}"
            for row in rows
        ]

    def load_foods():
        cursor = con.cursor()

        cursor.execute("""
        SELECT food_id, food_name
        FROM food_items
        WHERE availability='Available'
        ORDER BY food_name
        """)

        rows = cursor.fetchall()

        cursor.close()

        food_combo["values"] = [
            f"{row[0]} - {row[1]}"
            for row in rows
        ]

    def calculate_total():
        if food_combo.get() == "":
            messagebox.showwarning(
                "Warning",
                "Select a food item"
            )
            return

        try:
            quantity = int(
                quantity_entry.get()
            )

            if quantity <= 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Warning",
                "Enter valid quantity"
            )
            return

        food_id = int(
            food_combo.get().split(" - ")[0]
        )

        cursor = con.cursor()

        cursor.execute(
            "SELECT price FROM food_items WHERE food_id=%s",
            (food_id,)
        )

        result = cursor.fetchone()
        cursor.close()

        if result:
            total = float(result[0]) * quantity

            total_label.config(
                text=f"₹ {total:.2f}"
            )

    def place_order():
        if customer_combo.get() == "":
            messagebox.showwarning(
                "Warning",
                "Select a customer"
            )
            return

        if food_combo.get() == "":
            messagebox.showwarning(
                "Warning",
                "Select a food item"
            )
            return

        try:
            quantity = int(
                quantity_entry.get()
            )

            if quantity <= 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Warning",
                "Enter valid quantity"
            )
            return

        customer_id = int(
            customer_combo.get().split(" - ")[0]
        )

        food_id = int(
            food_combo.get().split(" - ")[0]
        )

        cursor = con.cursor()

        cursor.execute(
            "SELECT price FROM food_items WHERE food_id=%s",
            (food_id,)
        )

        result = cursor.fetchone()

        if not result:
            cursor.close()
            return

        price = float(result[0])
        total = price * quantity

        cursor.execute(
            """
            INSERT INTO orders
            (customer_id, total_amount)
            VALUES (%s, %s)
            """,
            (
                customer_id,
                total
            )
        )

        order_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO order_details
            (order_id, food_id, quantity, price, subtotal)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                order_id,
                food_id,
                quantity,
                price,
                total
            )
        )

        cursor.execute(
            """
            INSERT INTO sales
            (order_id, amount, payment_method)
            VALUES (%s, %s, %s)
            """,
            (
                order_id,
                total,
                "Cash"
            )
        )

        con.commit()
        cursor.close()

        messagebox.showinfo(
            "Success",
            "Order Placed Successfully"
        )

        customer_combo.set("")
        food_combo.set("")
        quantity_entry.delete(0, tk.END)

        total_label.config(
            text="₹ 0"
        )

        load_orders()

    def load_orders():
        for item in order_table.get_children():
            order_table.delete(item)

        cursor = con.cursor()

        cursor.execute("""
        SELECT
            o.order_id,
            c.customer_name,
            f.food_name,
            od.quantity,
            od.price,
            o.total_amount
        FROM orders o
        JOIN customers c
            ON o.customer_id = c.customer_id
        JOIN order_details od
            ON o.order_id = od.order_id
        JOIN food_items f
            ON od.food_id = f.food_id
        ORDER BY o.order_id DESC
        """)

        rows = cursor.fetchall()

        for row in rows:
            order_table.insert(
                "",
                tk.END,
                values=row
            )

        cursor.close()

    tk.Button(
        button_frame,
        text="Calculate Total",
        command=calculate_total,
        bg="#16324F",
        fg="white",
        font=("Arial", 11, "bold"),
        width=15,
        height=2
    ).pack(side="left", padx=6)

    tk.Button(
        button_frame,
        text="Place Order",
        command=place_order,
        bg="#16a34a",
        fg="white",
        font=("Arial", 11, "bold"),
        width=15,
        height=2
    ).pack(side="left", padx=6)

    tk.Button(
        button_frame,
        text="Exit",
        command=show_dashboard,
        bg="#374151",
        fg="white",
        font=("Arial", 11, "bold"),
        width=15,
        height=2
    ).pack(side="left", padx=6)

    load_customers()
    load_foods()
    load_orders()

def sales_window():

    clear_content()
    set_active(sales_btn)

    content_frame.configure(bg="#f4f7fb")

    header = tk.Frame(
        content_frame,
        bg="#17395C",
        height=60
    )
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Sales Analytics",
        font=("Arial", 21, "bold"),
        bg="#17395C",
        fg="white"
    ).pack(side="left", padx=22, pady=13)

    tk.Button(
        header,
        text="Exit",
        command=show_dashboard,
        bg="#374151",
        fg="white",
        font=("Arial", 9, "bold"),
        width=8
    ).pack(side="right", padx=18)

    filter_frame = tk.Frame(
        content_frame,
        bg="white",
        bd=1,
        relief="solid"
    )
    filter_frame.pack(
        fill="x",
        padx=15,
        pady=7
    )

    tk.Label(
        filter_frame,
        text="Date Range",
        bg="white",
        font=("Arial", 9, "bold")
    ).pack(side="left", padx=(8, 3))

    date_range_combo = ttk.Combobox(
        filter_frame,
        values=[
            "Today",
            "Yesterday",
            "Last 7 Days",
            "Last 30 Days",
            "This Month",
            "Custom Range"
        ],
        width=14,
        state="readonly"
    )

    date_range_combo.pack(side="left", padx=3)
    date_range_combo.set("Last 7 Days")

    tk.Label(
        filter_frame,
        text="Category",
        bg="white",
        font=("Arial", 9, "bold")
    ).pack(side="left", padx=(8, 3))

    category_combo = ttk.Combobox(
        filter_frame,
        width=13,
        state="readonly"
    )
    category_combo.pack(side="left", padx=3)

    tk.Label(
        filter_frame,
        text="Food",
        bg="white",
        font=("Arial", 9, "bold")
    ).pack(side="left", padx=(7, 3))

    food_combo = ttk.Combobox(
        filter_frame,
        width=15,
        state="readonly"
    )
    food_combo.pack(side="left", padx=3)

    tk.Label(
        filter_frame,
        text="Payment",
        bg="white",
        font=("Arial", 9, "bold")
    ).pack(side="left", padx=(7, 3))

    payment_combo = ttk.Combobox(
        filter_frame,
        width=10,
        state="readonly"
    )
    payment_combo.pack(side="left", padx=3)

    cards_frame = tk.Frame(
        content_frame,
        bg="#f4f7fb",
        height=78
    )
    cards_frame.pack(
        fill="x",
        padx=15,
        pady=3
    )
    cards_frame.pack_propagate(False)

    charts_frame = tk.Frame(
        content_frame,
        bg="#f4f7fb"
    )
    charts_frame.pack(
        fill="both",
        expand=True,
        padx=15
    )

    def load_foods_by_category(event=None):

        category = category_combo.get()

        cursor = con.cursor()

        if category == "All":

            cursor.execute("""
                SELECT DISTINCT food_name
                FROM food_items
                ORDER BY food_name
            """)

        else:

            cursor.execute("""
                SELECT DISTINCT food_name
                FROM food_items
                WHERE category = %s
                ORDER BY food_name
            """, (category,))

        food_values = [
            row[0]
            for row in cursor.fetchall()
        ]

        cursor.close()

        food_combo["values"] = ["All"] + food_values
        food_combo.set("All")

    category_combo.bind(
        "<<ComboboxSelected>>",
        load_foods_by_category
    )

    def get_date_range():

        today = datetime.now().date()
        selected = date_range_combo.get()

        if selected == "Today":
            return today, today

        elif selected == "Yesterday":
            yesterday = today - timedelta(days=1)
            return yesterday, yesterday

        elif selected == "Last 7 Days":
            return today - timedelta(days=6), today

        elif selected == "Last 30 Days":
            return today - timedelta(days=29), today

        elif selected == "This Month":
            first_day = today.replace(day=1)
            return first_day, today

        return None, None

    def load_analytics():

        for widget in cards_frame.winfo_children():
            widget.destroy()

        for widget in charts_frame.winfo_children():
            widget.destroy()

        start_date, end_date = get_date_range()

        if start_date is None or end_date is None:
            messagebox.showinfo(
                "Date Range",
                "Custom Range will be added next."
            )
            return

        start_date = str(start_date)
        end_date = str(end_date)

        category = category_combo.get()
        food = food_combo.get()
        payment = payment_combo.get()

        if payment == "💵 Cash":
            payment = "Cash"
        elif payment == "📱 UPI":
            payment = "UPI"
        elif payment == "💳 Card":
            payment = "Card"


        conditions = [
            "DATE(s.sale_date) BETWEEN %s AND %s"
        ]

        params = [
            start_date,
            end_date
        ]

        if payment != "All":
            conditions.append(
                "LOWER(TRIM(s.payment_method)) = LOWER(TRIM(%s))"
            )

            params.append(payment)

        if category != "All":

            conditions.append("""
                EXISTS (
                    SELECT 1
                    FROM order_details od2
                    JOIN food_items f2
                    ON od2.food_id = f2.food_id
                    WHERE od2.order_id = s.order_id
                    AND f2.category = %s
                )
            """)

            params.append(category)

        if food != "All":

            conditions.append("""
                EXISTS (
                    SELECT 1
                    FROM order_details od3
                    JOIN food_items f3
                    ON od3.food_id = f3.food_id
                    WHERE od3.order_id = s.order_id
                    AND f3.food_name = %s
                )
            """)

            params.append(food)

        where_clause = " AND ".join(conditions)

        cursor = con.cursor()

        try:

            cursor.execute(
                f"""
                SELECT
                    COALESCE(SUM(s.amount), 0),
                    COUNT(DISTINCT s.sale_id),
                    COALESCE(AVG(s.amount), 0)
                FROM sales s
                WHERE {where_clause}
                """,
                params
            )

            result = cursor.fetchone()

            total_sales = float(result[0] or 0)
            total_orders = int(result[1] or 0)
            average_order = float(result[2] or 0)

            cursor.execute(
                f"""
                SELECT
                    f.food_name,
                    SUM(od.quantity)
                FROM sales s
                JOIN order_details od
                ON s.order_id = od.order_id
                JOIN food_items f
                ON od.food_id = f.food_id
                WHERE {where_clause}
                GROUP BY f.food_id, f.food_name
                ORDER BY SUM(od.quantity) DESC
                LIMIT 1
                """,
                params
            )

            top_result = cursor.fetchone()

            top_food = (
                top_result[0]
                if top_result
                else "No Data"
            )

            top_quantity = (
                int(top_result[1])
                if top_result
                else 0
            )

            cards = [
                (
                    "Total Sales",
                    f"₹ {total_sales:.2f}",
                    "#D1FAE5",
                    "#047857"
                ),
                (
                    "Total Orders",
                    str(total_orders),
                    "#DBEAFE",
                    "#2563EB"
                ),
                (
                    "Average Order",
                    f"₹ {average_order:.2f}",
                    "#FEF3C7",
                    "#D97706"
                ),
                (
                    "Top Selling",
                    top_food,
                    "#EDE9FE",
                    "#7C3AED"
                )
            ]

            for title, value, bg, fg in cards:

                card = tk.Frame(
                    cards_frame,
                    bg=bg
                )

                card.pack(
                    side="left",
                    fill="both",
                    expand=True,
                    padx=4
                )

                tk.Label(
                    card,
                    text=title,
                    font=("Arial", 9, "bold"),
                    bg=bg
                ).pack(pady=(5, 1))

                tk.Label(
                    card,
                    text=value,
                    font=("Arial", 14, "bold"),
                    bg=bg,
                    fg=fg
                ).pack()

                if title == "Top Selling":

                    tk.Label(
                        card,
                        text=f"{top_quantity} sold",
                        font=("Arial", 8),
                        bg=bg
                    ).pack()

            chart_frames = []

            for r in range(2):

                for c in range(2):

                    frame = tk.Frame(
                        charts_frame,
                        bg="white",
                        bd=1,
                        relief="solid"
                    )

                    frame.grid(
                        row=r,
                        column=c,
                        sticky="nsew",
                        padx=4,
                        pady=4
                    )

                    chart_frames.append(frame)

            charts_frame.grid_rowconfigure(0, weight=1)
            charts_frame.grid_rowconfigure(1, weight=1)
            charts_frame.grid_columnconfigure(0, weight=1)
            charts_frame.grid_columnconfigure(1, weight=1)

            titles = [
                "Sales Trend",
                "Sales by Category",
                "Top Selling Food Items",
                "Recent Sales"
            ]

            for frame, title in zip(
                chart_frames,
                titles
            ):

                tk.Label(
                    frame,
                    text=title,
                    font=("Arial", 10, "bold"),
                    bg="white",
                    fg="#17395C"
                ).pack(
                    anchor="w",
                    padx=8,
                    pady=3
                )

            # SALES TREND

            cursor.execute(
                f"""
                SELECT
                    DATE(s.sale_date),
                    SUM(s.amount)
                FROM sales s
                WHERE {where_clause}
                GROUP BY DATE(s.sale_date)
                ORDER BY DATE(s.sale_date)
                """,
                params
            )

            trend_data = cursor.fetchall()

            if trend_data:

                dates = [
                    str(row[0])
                    for row in trend_data
                ]

                amounts = [
                    float(row[1])
                    for row in trend_data
                ]

                fig, ax = plt.subplots(
                    figsize=(4.1, 1.7)
                )

                ax.plot(
                    dates,
                    amounts,
                    marker="o",
                    linewidth=2
                )

                ax.set_ylabel(
                    "Sales ₹",
                    fontsize=7
                )

                ax.tick_params(
                    labelsize=6,
                    axis="x",
                    rotation=25
                )

                ax.grid(
                    True,
                    alpha=0.3
                )

                fig.tight_layout()

                canvas = FigureCanvasTkAgg(
                    fig,
                    master=chart_frames[0]
                )

                canvas.draw()

                canvas.get_tk_widget().pack(
                    fill="both",
                    expand=True
                )

            else:

                tk.Label(
                    chart_frames[0],
                    text="No Data Available",
                    font=("Arial", 11),
                    bg="white",
                    fg="#777777"
                ).pack(expand=True)

            # CATEGORY CHART

            cursor.execute(
                f"""
                SELECT
                    f.category,
                    SUM(od.quantity * od.price)
                FROM sales s
                JOIN order_details od
                ON s.order_id = od.order_id
                JOIN food_items f
                ON od.food_id = f.food_id
                WHERE {where_clause}
                GROUP BY f.category
                ORDER BY SUM(od.quantity * od.price) DESC
                """,
                params
            )

            category_data = cursor.fetchall()

            if category_data:

                labels = [
                    row[0] or "Other"
                    for row in category_data
                ]

                values = [
                    float(row[1])
                    for row in category_data
                ]

                fig, ax = plt.subplots(
                    figsize=(4.1, 1.7)
                )

                ax.pie(
                    values,
                    labels=labels,
                    autopct="%1.0f%%",
                    textprops={
                        "fontsize": 6
                    }
                )

                fig.tight_layout()

                canvas = FigureCanvasTkAgg(
                    fig,
                    master=chart_frames[1]
                )

                canvas.draw()

                canvas.get_tk_widget().pack(
                    fill="both",
                    expand=True
                )

            else:

                tk.Label(
                    chart_frames[1],
                    text="No Data Available",
                    font=("Arial", 11),
                    bg="white",
                    fg="#777777"
                ).pack(expand=True)

            # TOP SELLING FOOD

            cursor.execute(
                f"""
                SELECT
                    f.food_name,
                    SUM(od.quantity)
                FROM sales s
                JOIN order_details od
                ON s.order_id = od.order_id
                JOIN food_items f
                ON od.food_id = f.food_id
                WHERE {where_clause}
                GROUP BY f.food_id, f.food_name
                ORDER BY SUM(od.quantity) DESC
                LIMIT 6
                """,
                params
            )

            food_data = cursor.fetchall()

            if food_data:

                food_names = [
                    row[0]
                    for row in food_data
                ]

                quantities = [
                    int(row[1])
                    for row in food_data
                ]

                fig, ax = plt.subplots(
                    figsize=(4.1, 1.7)
                )

                ax.pie(
                    quantities,
                    labels=food_names,
                    autopct="%1.0f%%",
                    wedgeprops={
                        "width": 0.45
                    },
                    textprops={
                        "fontsize": 6
                    }
                )

                fig.tight_layout()

                canvas = FigureCanvasTkAgg(
                    fig,
                    master=chart_frames[2]
                )

                canvas.draw()

                canvas.get_tk_widget().pack(
                    fill="both",
                    expand=True
                )

            else:

                tk.Label(
                    chart_frames[2],
                    text="No Data Available",
                    font=("Arial", 11),
                    bg="white",
                    fg="#777777"
                ).pack(expand=True)

            # RECENT SALES

            cursor.execute(
                f"""
                SELECT
                    s.order_id,
                    s.amount
                FROM sales s
                WHERE {where_clause}
                ORDER BY s.sale_id DESC
                LIMIT 8
                """,
                params
            )

            recent_data = cursor.fetchall()

            if recent_data:

                order_ids = [
                    str(row[0])
                    for row in recent_data
                ]

                amounts = [
                    float(row[1])
                    for row in recent_data
                ]

                fig, ax = plt.subplots(
                    figsize=(4.1, 1.7)
                )

                ax.bar(
                    order_ids,
                    amounts
                )

                ax.set_xlabel(
                    "Order ID",
                    fontsize=7
                )

                ax.set_ylabel(
                    "Amount ₹",
                    fontsize=7
                )

                ax.tick_params(
                    labelsize=6
                )

                ax.grid(
                    axis="y",
                    alpha=0.3
                )

                fig.tight_layout()

                canvas = FigureCanvasTkAgg(
                    fig,
                    master=chart_frames[3]
                )

                canvas.draw()

                canvas.get_tk_widget().pack(
                    fill="both",
                    expand=True
                )

            else:

                tk.Label(
                    chart_frames[3],
                    text="No Data Available",
                    font=("Arial", 11),
                    bg="white",
                    fg="#777777"
                ).pack(expand=True)

        except Exception as e:

            messagebox.showerror(
                "Sales Analytics Error",
                str(e)
            )

        finally:

            cursor.close()

    cursor = con.cursor()

    cursor = con.cursor()

    cursor.execute("""
        SELECT DISTINCT category
        FROM food_items
        WHERE category IS NOT NULL
        ORDER BY category
    """)

    categories = [row[0] for row in cursor.fetchall()]

    cursor.execute("""
        SELECT DISTINCT food_name
        FROM food_items
        ORDER BY food_name
    """)

    foods = [row[0] for row in cursor.fetchall()]

    cursor.execute("""
        SELECT DISTINCT payment_method
        FROM sales
        WHERE payment_method IS NOT NULL
        ORDER BY payment_method
    """)

    payments = [row[0] for row in cursor.fetchall()]

    cursor.close()

    category_combo["values"] = ["All"] + categories
    food_combo["values"] = ["All"] + foods
    payment_combo["values"] = [
        "All",
        "💵 Cash",
        "📱 UPI",
        "💳 Card"
    ]

    category_combo.set("All")
    food_combo.set("All")
    payment_combo.set("All")

    tk.Button(
        filter_frame,
        text="Apply",
        command=load_analytics,
        bg="#2563EB",
        fg="white",
        font=("Arial", 9, "bold"),
        width=8
    ).pack(side="left", padx=5)

    def reset_filters():

        date_range_combo.set("Last 7 Days")
        category_combo.set("All")
        food_combo.set("All")
        payment_combo.set("All")

        load_analytics()

    tk.Button(
        filter_frame,
        text="Reset",
        command=reset_filters,
        bg="#6B7280",
        fg="white",
        font=("Arial", 9, "bold"),
        width=8
    ).pack(side="left", padx=3)

    load_analytics()


def create_dashboard_charts(parent):

    charts_frame = tk.Frame(
        parent,
        bg="#eef3f8"
    )
    charts_frame.pack(
        fill="x",
        padx=35,
        pady=15
    )

    pie_frame = tk.Frame(
        charts_frame,
        bg="white",
        width=300,
        height=250
    )
    pie_frame.pack(
        side="left",
        expand=True,
        fill="both",
        padx=8
    )
    pie_frame.pack_propagate(False)

    bar_frame = tk.Frame(
        charts_frame,
        bg="white",
        width=300,
        height=250
    )
    bar_frame.pack(
        side="left",
        expand=True,
        fill="both",
        padx=8
    )
    bar_frame.pack_propagate(False)

    graph_frame = tk.Frame(
        charts_frame,
        bg="white",
        width=300,
        height=250
    )
    graph_frame.pack(
        side="left",
        expand=True,
        fill="both",
        padx=8
    )
    graph_frame.pack_propagate(False)

    cursor = con.cursor()

    cursor.execute("""
    SELECT
        f.food_name,
        SUM(od.quantity)
    FROM order_details od
    JOIN food_items f
        ON od.food_id = f.food_id
    GROUP BY f.food_id, f.food_name
    ORDER BY SUM(od.quantity) DESC
    """)

    food_rows = cursor.fetchall()

    cursor.execute("""
    SELECT
        sale_id,
        amount
    FROM sales
    ORDER BY sale_id
    """)

    sales_rows = cursor.fetchall()

    cursor.close()

    if food_rows:

        food_names = [
            row[0]
            for row in food_rows
        ]

        food_quantity = [
            float(row[1])
            for row in food_rows
        ]

        fig1, ax1 = plt.subplots(
            figsize=(3.2, 2.4)
        )

        ax1.pie(
            food_quantity,
            autopct="%1.0f%%",
            startangle=90,
            textprops={"fontsize": 7}
        )

        ax1.set_title(
            "Food Order Distribution",
            fontsize=10,
            fontweight="bold"
        )

        ax1.legend(
            food_names,
            loc="lower center",
            bbox_to_anchor=(0.5, -0.18),
            fontsize=6,
            ncol=2
        )

        fig1.tight_layout()

        canvas1 = FigureCanvasTkAgg(
            fig1,
            master=pie_frame
        )

        canvas1.draw()

        canvas1.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        fig2, ax2 = plt.subplots(
            figsize=(3.2, 2.4)
        )

        ax2.bar(
            food_names,
            food_quantity
        )

        ax2.set_title(
            "Top Selling Food Items",
            fontsize=10,
            fontweight="bold"
        )

        ax2.set_xlabel(
            "Food",
            fontsize=8
        )

        ax2.set_ylabel(
            "Quantity",
            fontsize=8
        )

        ax2.tick_params(
            axis="x",
            labelrotation=35,
            labelsize=7
        )

        fig2.tight_layout()

        canvas2 = FigureCanvasTkAgg(
            fig2,
            master=bar_frame
        )

        canvas2.draw()

        canvas2.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    if sales_rows:

        sale_ids = [
            row[0]
            for row in sales_rows
        ]

        amounts = [
            float(row[1])
            for row in sales_rows
        ]

        fig3, ax3 = plt.subplots(
            figsize=(3.2, 2.4)
        )

        ax3.plot(
            sale_ids,
            amounts,
            marker="o",
            linewidth=2
        )

        ax3.set_title(
            "Sales Trend",
            fontsize=10,
            fontweight="bold"
        )

        ax3.set_xlabel(
            "Sale ID",
            fontsize=8
        )

        ax3.set_ylabel(
            "Amount",
            fontsize=8
        )

        ax3.tick_params(
            labelsize=7
        )

        ax3.grid(True)

        fig3.tight_layout()

        canvas3 = FigureCanvasTkAgg(
            fig3,
            master=graph_frame
        )

        canvas3.draw()

        canvas3.get_tk_widget().pack(
            fill="both",
            expand=True
        )

def show_dashboard():

    clear_content()
    set_active(dashboard_btn)

    main_frame = content_frame
    main_frame.configure(bg="#eaf2f8")

    # ================= TOP HEADER =================

    top_frame = tk.Frame(
        main_frame,
        bg="#16324F",
        height=85
    )
    top_frame.pack(
        fill="x"
    )
    top_frame.pack_propagate(False)

    title_frame = tk.Frame(
        top_frame,
        bg="#16324F"
    )
    title_frame.pack(
        side="left",
        padx=30,
        pady=12
    )

    tk.Label(
        top_frame,
        text="FOOD ORDER MANAGEMENT AND SALES ANALYTICS SYSTEM",
        font=("Arial", 20, "bold"),
        bg="#16324F",
        fg="white"
    ).pack(
        side="left",
        padx=10
    )
    # ================= BUTTONS =================

    button_frame = tk.Frame(
        top_frame,
        bg="#16324F"
    )
    button_frame.pack(
        side="right",
        padx=25
    )

    tk.Button(
        button_frame,
        text="⟳ Refresh",
        command=show_dashboard,
        bg="#2563eb",
        fg="white",
        font=("Arial", 11, "bold"),
        width=9,
        height=2,
        relief="flat",
        cursor="hand2"
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        button_frame,
        text="Logout",
        command=logout,
        bg="#dc2626",
        fg="white",
        font=("Arial", 11, "bold"),
        width=9,
        height=2,
        relief="flat",
        cursor="hand2"
    ).pack(
        side="left",
        padx=5
    )

    # ================= WELCOME =================

    welcome_frame = tk.Frame(
        main_frame,
        bg="#eaf2f8"
    )
    welcome_frame.pack(
        fill="x",
        padx=35,
        pady=(18, 8)
    )

    tk.Label(
        welcome_frame,
        text="Welcome to Your Food Management Hub! 👋",
        font=("Arial", 20, "bold"),
        bg="#eaf2f8",
        fg="#16324F"
    ).pack(
        anchor="w"
    )

    tk.Label(
        welcome_frame,
        text="Manage customers, food items, orders and sales efficiently in one place.",
        font=("Arial", 11),
        bg="#eaf2f8",
        fg="#666666"
    ).pack(
        anchor="w",
        pady=(4, 0)
    )

    # ================= FOOD BANNER =================

    hero_frame = tk.Frame(
        main_frame,
        bg="#dbeafe",
        height=125
    )
    hero_frame.pack(
        fill="x",
        padx=35,
        pady=10
    )
    hero_frame.pack_propagate(False)

    hero_left = tk.Frame(
        hero_frame,
        bg="#dbeafe"
    )
    hero_left.pack(
        side="left",
        fill="both",
        expand=True,
        padx=25,
        pady=15
    )

    tk.Label(
        hero_left,
        text="Fresh Food. Easy Orders. Smart Management.",
        font=("Arial", 17, "bold"),
        bg="#dbeafe",
        fg="#16324F"
    ).pack(
        anchor="w"
    )

    tk.Label(
        hero_left,
        text="Everything you need to manage your food ordering system.",
        font=("Arial", 10),
        bg="#dbeafe",
        fg="#555555"
    ).pack(
        anchor="w",
        pady=5
    )

    tk.Label(
        hero_frame,
        text="🍕  🍔  🍟  🍗  🍜  🍛",
        font=("Arial", 28),
        bg="#dbeafe"
    ).pack(
        side="right",
        padx=25
    )

    # ================= SUMMARY CARDS =================

    cursor = con.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM customers"
    )
    total_customers = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM food_items"
    )
    total_food_items = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM orders"
    )
    total_orders = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM sales"
    )
    total_sales = cursor.fetchone()[0]

    cursor.close()

    summary_title = tk.Label(
        main_frame,
        text="System Overview",
        font=("Arial", 17, "bold"),
        bg="#eaf2f8",
        fg="#16324F"
    )
    summary_title.pack(
        anchor="w",
        padx=35,
        pady=(8, 5)
    )

    summary_frame = tk.Frame(
        main_frame,
        bg="#eaf2f8"
    )
    summary_frame.pack(
        fill="x",
        padx=30
    )

    summary_data = [
        (
            "👥",
            "Total Customers",
            str(total_customers),
            "#d1fae5",
            "#047857"
        ),
        (
            "🍴",
            "Food Items",
            str(total_food_items),
            "#dbeafe",
            "#1d4ed8"
        ),
        (
            "🛒",
            "Total Orders",
            str(total_orders),
            "#fef3c7",
            "#b45309"
        ),
        (
            "💰",
            "Total Sales",
            f"₹ {total_sales:.2f}",
            "#ede9fe",
            "#6d28d9"
        )
    ]

    for icon, title, value, bg_color, text_color in summary_data:

        card = tk.Frame(
            summary_frame,
            bg=bg_color,
            height=100,
            highlightbackground="white",
            highlightthickness=1
        )

        card.pack(
            side="left",
            expand=True,
            fill="x",
            padx=6
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=icon,
            font=("Arial", 24),
            bg=bg_color
        ).pack(
            pady=(7, 0)
        )

        tk.Label(
            card,
            text=value,
            font=("Arial", 17, "bold"),
            bg=bg_color,
            fg=text_color
        ).pack()

        tk.Label(
            card,
            text=title,
            font=("Arial", 9, "bold"),
            bg=bg_color,
            fg="#555555"
        ).pack()

    # ================= FOOD COLLECTION =================

    tk.Label(
        main_frame,
        text="Our Food Collection",
        font=("Arial", 17, "bold"),
        bg="#eaf2f8",
        fg="#16324F"
    ).pack(
        anchor="w",
        padx=35,
        pady=(13, 5)
    )

    food_frame = tk.Frame(
        main_frame,
        bg="#eaf2f8"
    )
    food_frame.pack(
        padx=30
    )

    foods = [
        ("🍕", "Pizza", "#fee2e2"),
        ("🍔", "Burger", "#fef3c7"),
        ("🍟", "Fries", "#fef9c3"),
        ("🍗", "Chicken", "#ffedd5"),
        ("🍜", "Noodles", "#fce7f3"),
        ("🍛", "Biryani", "#dcfce7"),
        ("🌮", "Tacos", "#dbeafe"),
        ("🥗", "Salad", "#d1fae5"),
        ("🍰", "Dessert", "#f3e8ff"),
        ("🍩", "Donut", "#fce7f3"),
        ("🍦", "Ice Cream", "#e0f2fe"),
        ("🥤", "Drinks", "#cffafe")
    ]

    for i, (icon, name, color) in enumerate(foods):

        card = tk.Frame(
            food_frame,
            bg=color,
            width=125,
            height=68,
            highlightbackground="#ffffff",
            highlightthickness=1
        )

        card.grid(
            row=i // 6,
            column=i % 6,
            padx=6,
            pady=5
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=icon,
            font=("Arial", 21),
            bg=color
        ).pack(
            pady=(2, 0)
        )

        tk.Label(
            card,
            text=name,
            font=("Arial", 9, "bold"),
            bg=color,
            fg="#333333"
        ).pack()

    # ================= FOOTER =================

    tk.Label(
        main_frame,
        text="Everything you need for smooth food order management.",
        font=("Arial", 9, "italic"),
        bg="#eaf2f8",
        fg="#777777"
    ).pack(
        pady=(7, 5)
    )

logo = tk.Label(
    sidebar,
    text="FOOD ORDER",
    font=("Arial", 20, "bold"),
    bg="#16324F",
    fg="white"
)
logo.pack(
    pady=(40, 5)
)

sub_logo = tk.Label(
    sidebar,
    text="MANAGEMENT SYSTEM",
    font=("Arial", 10),
    bg="#16324F",
    fg="white"
)
sub_logo.pack(
    pady=(0, 35)
)

dashboard_btn = tk.Button(
    sidebar,
    text="Dashboard",
    font=("Arial", 12),
    bg="#285A7A",
    fg="white",
    bd=0,
    width=20,
    pady=12,
    command=show_dashboard
)
dashboard_btn.pack(
    pady=5
)

customer_btn = tk.Button(
    sidebar,
    text="Customers",
    font=("Arial", 12),
    bg="#16324F",
    fg="white",
    bd=0,
    width=20,
    pady=12,
    command=customer_window
)
customer_btn.pack(
    pady=2
)

food_btn = tk.Button(
    sidebar,
    text="Food Items",
    font=("Arial", 12),
    bg="#16324F",
    fg="white",
    bd=0,
    width=20,
    pady=12,
    command=food_window
)
food_btn.pack(
    pady=2
)

order_btn = tk.Button(
    sidebar,
    text="Orders",
    font=("Arial", 12),
    bg="#16324F",
    fg="white",
    bd=0,
    width=20,
    pady=12,
    command=order_window
)
order_btn.pack(
    pady=2
)

sales_btn = tk.Button(
    sidebar,
    text="Sales Analytics",
    font=("Arial", 12),
    bg="#16324F",
    fg="white",
    bd=0,
    width=20,
    pady=12,
    command=sales_window
)
sales_btn.pack(
    pady=2
)

tk.Button(
    login_window,
    text="Login",
    command=login,
    width=15
).pack(
    pady=20
)

root.withdraw()

show_dashboard()

root.mainloop()