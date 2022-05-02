from ast import Or, Return
from hmac import new
from tkinter import *
from tkinter import ttk
import sqlite3, csv
import tkinter.font as font
import types
import pandas as pd
from setuptools import Command
from sympy import expand
from datetime import date, timedelta, datetime

#create tkinter window
win = Tk()
win.geometry("500x500")
win.title('CAR RENTAL')
root = Frame(win)
root.pack(side="top", expand=True, fill="both")

def reset_root():
    for widgets in root.winfo_children():
          widgets.destroy()

#this function is to create the database schema and import data from CSV files
def create_db():

    #connect to DB and create a table
    conn = sqlite3.connect('car_rental.db')
    print("connected to DB successfully")

    #create cursor
    c = conn.cursor()

    #create tables
    c.execute('''
    DROP TABLE IF EXISTS CUSTOMER
    ''')
    c.execute('''
    DROP TABLE IF EXISTS VEHICLE
    ''')
    c.execute('''
    DROP TABLE IF EXISTS RATE
    ''')
    c.execute('''
    DROP TABLE IF EXISTS RENTAL
    ''')
    c.execute('''
    CREATE TABLE CUSTOMER
    (
        CustID INTEGER NOT NULL,
        Name VARCHAR(160) NOT NULL,
        Phone VARCHAR(15) NOT NULL,

        CONSTRAINT PK_Customer PRIMARY KEY (CustID)
    )
    ''')
    c.execute('''
    CREATE TABLE VEHICLE
    (
        VehicleID VARCHAR(30) NOT NULL,
        Description VARCHAR(100) NOT NULL,
        Year VARCHAR(4) NOT NULL,
        Type INTEGER NOT NULL,
        Category INTEGER NOT NULL,

        CONSTRAINT PK_Vehicle PRIMARY KEY (VehicleID),

        FOREIGN KEY (Type) REFERENCES RATE (Type)
        ON DELETE NO ACTION ON UPDATE CASCADE
    )
    ''')
    c.execute('''
    CREATE TABLE RATE
    (
        Type INTEGER NOT NULL,
        Category INTEGER NOT NULL,
        Weekly REAL NOT NULL,
        Daily REAL NOT NULL,

        CONSTRAINT PK_Rate PRIMARY KEY (Type, Category)
    )
    ''')
    c.execute('''
    CREATE TABLE RENTAL
    (
        CustID INTEGER NOT NULL,
        VehicleID INTEGER NOT NULL,
        StartDate DATE NOT NULL,
        OrderDate DATE NOT NULL,
        RentalType INTEGER NOT NULL,
        Qty INTEGER NOT NULL,
        ReturnDate DATE NOT NULL,
        TotalAmount INTEGER NOT NULL,
        PaymentDate DATE,

        CONSTRAINT PK_Rental PRIMARY KEY (CustID, VehicleID, StartDate),

        FOREIGN KEY (CustID) REFERENCES CUSTOMER (CustID)
        ON DELETE CASCADE ON UPDATE CASCADE

        FOREIGN KEY (VehicleID) REFERENCES VEHICLE (VehicleID)
        ON DELETE CASCADE ON UPDATE CASCADE
    )
    ''')

    #read data from csv files
    df = pd.read_csv("CUSTOMER.csv")
    df.to_sql("CUSTOMER", conn, if_exists='append', index=False)
    df = pd.read_csv("RATE.csv")
    df.to_sql("RATE", conn, if_exists='append', index=False)
    df = pd.read_csv("RENTAL.csv", na_filter=False)
    df.to_sql("RENTAL", conn, if_exists='append', index=False)
    df = pd.read_csv("VEHICLE.csv")
    df.to_sql("VEHICLE", conn, if_exists='append', index=False)

    print("created tables successfuly!")
    #commint changes and close cursor
    conn.commit()
    conn.close()

def add_new_cust():
    reset_root()

    name_label = Label(root, text = 'name: ')
    name_label.grid(row = 0, column = 0, padx = (100,0))
    Name = Entry(root, width = 30)
    Name.grid(row = 0, column = 1, padx = 20)

    phone_label = Label(root, text = 'phone: ')
    phone_label.grid(row =1, column = 0, padx = (100,0))
    Phone = Entry(root, width = 30)
    Phone.grid(row = 1, column = 1, padx = 20)

    submit_btn = Button(root, text = 'Submit', command = lambda: submit_cust(Name.get(), Phone.get()))
    submit_btn.grid(row = 2, column = 0, columnspan = 3, padx= 100)

    home_btn = Button(root, text = 'Home', command = pick_option)
    home_btn.grid(row = 3, column = 0, columnspan = 3, padx= 100, ipadx = 140)

def submit_cust(Name, Phone):
    conn = sqlite3.connect('car_rental.db')
    c = conn.cursor()
    c.execute("""INSERT INTO CUSTOMER(Name, Phone) VALUES (:Name, :Phone )""",
    {
        'Name' : Name,
        'Phone': Phone
    })
    conn.commit()
    conn.close()
    add_new_cust()


Types = [
   "Compact", "Medium", "Large", "SUV", "Truck", "VAN"
]
Type_dict = {
    "Compact" : 1,
    "Medium": 2,
    "Large": 3,
    "SUV": 4,
    "Truck": 5,
    "VAN": 6
}
Categories = [
    "Basic", "Luxury"
]
Category_dict = {
    "Basic" : 0,
    "Luxury" : 1
}

def add_new_car():
    reset_root()

    VIN_label = Label(root, text = 'Vehicle ID: ')
    VIN_label.grid(row =0, column = 0)
    VIN = Entry(root, width = 30)
    VIN.grid(row=0, column = 1, padx = 20)

    description_label = Label(root, text = 'Name: ')
    description_label.grid(row =1, column = 0)
    Description = Entry(root, width = 30)
    Description.grid(row = 1, column = 1, padx = 20)

    year_label = Label(root, text = 'Year: ')
    year_label.grid(row =2, column = 0)
    Year = Entry(root, width = 30)
    Year.grid(row = 2, column = 1, padx = 20)

    type_label = Label(root, text = 'Type: ' )
    type_label.grid(row = 3, column=0)
    Type = ttk.Combobox(root, values = Types)
    Type.grid(row = 3, column = 1, padx = 20)
    Type.current()

    category_label = Label(root, text = 'Category: ' )
    category_label.grid(row = 4, column=0)
    Category = ttk.Combobox(root, values = Categories)
    Category.grid(row = 4, column = 1, padx = 20)
    Category.current()

    submit_btn = Button(root, text = 'Submit', command = lambda: submit_car(VIN.get(), Description.get(), Year.get(), Type.get(), Category.get()))
    submit_btn.grid(row = 5, column = 0, columnspan = 3, padx= 100, ipadx = 140)
    home_btn = Button(root, text = 'Home', command = pick_option)
    home_btn.grid(row = 6, column = 0, columnspan = 3, padx= 100, ipadx = 140)

def submit_car(VIN, Description, Year, Type, Category):
    conn = sqlite3.connect('car_rental.db')
    c = conn.cursor()

    c.execute("""INSERT INTO VEHICLE VALUES (:VIN, :Description, :Year, :Type, :Category )""",
    {
        'VIN' : VIN,
        'Description': Description,
        'Year': Year,
        'Type' : Type_dict[Type],
        'Category' : Category_dict[Category]
    })
    conn.commit()
    conn.close()
    add_new_car()

RentalTypes = [ "Daily", "Weekly"]
RentalType_dict = {"Daily" : 1, "Weekly" : 7}
pay_options = ["now", "when return"]
new_cust = ["yes", "no"]

def add_new_rental():
    reset_root()

    type_label = Label(root, text = 'Type: ' )
    type_label.grid(row = 0, column=0)
    Type = ttk.Combobox(root, values = Types)
    Type.grid(row = 0, column = 1, padx = 20)
    Type.current()

    category_label = Label(root, text = 'Category: ' )
    category_label.grid(row = 1, column=0)
    Category = ttk.Combobox(root, values = Categories)
    Category.grid(row = 1, column = 1, padx = 20)
    Category.current()

    start_date_label = Label(root, text = 'start date: ')
    start_date_label.grid(row =2, column = 0)
    StartDate = Entry(root, width = 30)
    StartDate.grid(row=2, column = 1, padx = 20)

    RentalType_label = Label(root, text = 'Rental Type: ' )
    RentalType_label.grid(row = 3, column=0)
    RentalType = ttk.Combobox(root, values = RentalTypes)
    RentalType.grid(row = 3, column = 1, padx = 20)
    RentalType.current()

    Qty_label = Label(root, text = 'Quantity: ')
    Qty_label.grid(row = 4, column=0)
    Qty = Entry(root, width = 30)
    Qty.grid(row=4, column = 1, padx = 20)

    PaymentDate_label = Label(root, text = 'Payment Date: ' )
    PaymentDate_label.grid(row = 5, column=0)
    PaymentDate = ttk.Combobox(root, values = pay_options)
    PaymentDate.grid(row = 5, column = 1, padx = 20)
    PaymentDate.current()

    submit_btn = Button(root, text = 'Submit', command=lambda: show_available_car(Type.get(), Category.get(), StartDate.get(), RentalType.get(), Qty.get(), PaymentDate.get()))
    submit_btn.grid(row = 6, column = 0, columnspan = 3, padx= 100, ipadx = 140)
    home_btn = Button(root, text = 'Home', command = pick_option)
    home_btn.grid(row = 7, column = 0, columnspan = 3, padx= 100, ipadx = 140)

def show_available_car(Type, Category, StartDate, RentalType, Qty, PaymentDate):
    conn = sqlite3.connect('car_rental.db')
    c = conn.cursor()

    Days = int(RentalType_dict[RentalType] * int(Qty))
    OrderDate = date.today()
    StartDateFormatted = date.fromisoformat(StartDate)
    ReturnDate = StartDateFormatted + timedelta(days=Days)

    c.execute("""
    SELECT VehicleId, Description, Year, Weekly, Daily
    FROM VEHICLE V LEFT NATURAL JOIN RENTAL R NATURAL JOIN RATE
    WHERE Type = ? AND Category = ?
    AND V.VehicleID NOT IN (SELECT VehicleID FROM RENTAL
                            WHERE (StartDate >= ? AND StartDate <= ?)

                            OR (StartDate < ? AND ReturnDate > ?))
    """, (Type_dict[Type], Category_dict[Category], StartDate, ReturnDate, ReturnDate, StartDate))

    reset_root()
    available_cars = c.fetchall()

    info = "Type: " + Type + "\n" + "Category: " + Category + "\n" + "Weekly: " + str(available_cars[0][3]) + "\n" + "Daily: " + str(available_cars[0][4])
    info_label = Label(root, text = info)
    info_label.grid(row = 0, pady = 10)

    cars_listbox = Listbox(root)
    cars_listbox.grid(row = 1, padx = 50, pady = 20, ipadx = 50)

    for car in available_cars:
        cars_listbox.insert(END, car[1] + " | " + car[2])

    Weekly = available_cars[0][3]
    Daily = available_cars[0][4]
    TotalAmount = 0
    if(RentalType == "Daily"): TotalAmount = int(Daily) * int(Qty)
    else: TotalAmount = int(Weekly) * int(Qty)

    select_btn = Button(root, text = "Select", command= lambda: submit_rental(available_cars[cars_listbox.curselection()[0]][0], StartDate, OrderDate, RentalType, Qty, ReturnDate, TotalAmount, PaymentDate))
    select_btn.grid(row = 2, padx = 70)

    back_btn = Button(root, text = "Back", command=add_new_rental)
    back_btn.grid(row = 3, padx = 70)

    home_btn = Button(root, text = "Home", command=pick_option)
    home_btn.grid(row = 4, padx = 70)
    conn.commit()
    conn.close()


def submit_rental(VIN, StartDate, OrderDate, RentalType, Qty, ReturnDate, TotalAmount, PaymentDate):
    reset_root()

    name_label = Label(root, text = 'name: ')
    name_label.grid(row = 0, column = 0, padx = 20)
    Name = Entry(root, width = 30)
    Name.grid(row = 0, column = 1, padx = 10)

    phone_label = Label(root, text = 'phone: ')
    phone_label.grid(row =1, column = 0, padx = 20)
    Phone = Entry(root, width = 30)
    Phone.grid(row = 1, column = 1, padx = 10)

    newCust_label = Label(root, text = 'new customer: ' )
    newCust_label.grid(row = 2, column=0)
    NewCust = ttk.Combobox(root, values = new_cust)
    NewCust.grid(row = 2, column = 1, padx = 10)
    NewCust.current()


    submit_btn = Button(root, text = "Submit", command= lambda: add_rental_to_db(VIN, Name.get(), Phone.get(), NewCust.get(), StartDate, OrderDate, RentalType, Qty, ReturnDate, TotalAmount, PaymentDate))
    submit_btn.grid(row = 3, column= 1)

    cancel_btn = Button(root, text = "Cancel", command=add_new_rental)
    cancel_btn.grid(row = 4, column= 1)

    home_btn = Button(root, text = "Home", command=pick_option)
    home_btn.grid(row = 5, column= 1)

def add_rental_to_db(VIN, Name, Phone, NewCust, StartDate, OrderDate, RentalType, Qty, ReturnDate, TotalAmount, PaymentDate):
    reset_root()

    conn = sqlite3.connect('car_rental.db')
    c = conn.cursor()

    if(NewCust == "yes"):
        c.execute("""INSERT INTO CUSTOMER(Name, Phone) VALUES (:Name, :Phone )""",
        {
            'Name' : Name,
            'Phone': Phone
        })
    c.execute("SELECT CustId FROM CUSTOMER WHERE Name = ? AND Phone = ?", (Name, Phone))
    Custid = c.fetchall()[0][0]
    if(PaymentDate == 'now'): PaymentDate = date.today()
    else: PaymentDate = 'NULL'

    c.execute("""INSERT INTO RENTAL VALUES(:CustId, :VehicleId, :StartDate, :OrderDate, :RentalType, :Qty, :ReturnDate, :TotalAmount, :PaymentDate, 0)""",
    {
        'CustId' : Custid,
        'VehicleId': VIN,
        'StartDate': StartDate,
        'OrderDate': OrderDate,
        'RentalType': RentalType_dict[RentalType],
        'Qty' : Qty,
        'ReturnDate' : ReturnDate,
        'TotalAmount': TotalAmount,
        'PaymentDate': PaymentDate
    })

    conn.commit()
    conn.close()
    pick_option()

def return_car():
    reset_root()

    customer_name_label = Label(root, text = 'Customer Name: ')
    customer_name_label.grid(row = 0, column=0)
    CustomerName = Entry(root, width = 30)
    CustomerName.grid(row=0, column = 1, padx = 20)

    return_date_label = Label(root, text = 'Return date: ')
    return_date_label.grid(row =1, column = 0)
    ReturnDate = Entry(root, width = 30)
    ReturnDate.grid(row=1, column = 1, padx = 20)

    vehicle_id_label = Label(root, text = 'Vehicle ID: ')
    vehicle_id_label.grid(row = 2, column=0)
    VehicleID = Entry(root, width = 30)
    VehicleID.grid(row=2, column = 1, padx = 20)

    submit_btn = Button(root, text = 'Submit', command=lambda: show_rental( CustomerName.get(), VehicleID.get(), ReturnDate.get()))
    submit_btn.grid(row = 3, column = 0, columnspan = 3, padx= 100, ipadx = 140)
    home_btn = Button(root, text = 'Home', command = pick_option)
    home_btn.grid(row = 4, column = 0, columnspan = 3, padx= 100, ipadx = 140)

def show_rental(CustName, VID, ReturnDate):
    reset_root()

    conn = sqlite3.connect('car_rental.db')
    c = conn.cursor()

    c.execute("""SELECT CustID FROM Customer WHERE Name = ?""", (CustName,))
    CustID = c.fetchall()[0][0]

    c.execute("""
    SELECT TotalAmount, PaymentDate
    FROM Rental
    WHERE CustID = ? AND VehicleID = ? AND ReturnDate = ?""", (
    CustID, VID, ReturnDate))

    rental_info = c.fetchall()
    if (rental_info[0][1] == 'NULL'):
        payment_due = rental_info[0][0]
    else:
        payment_due = 0

    info = "Payment Due: " + str(payment_due)
    info_label = Label(root, text = info)
    info_label.grid(row = 0, pady = 10)

    back_btn = Button(root, text = "Back", command=return_car)
    back_btn.grid(row = 1, column = 0, columnspan = 3, padx = 100)
    #
    return_btn = Button(root, text = "Return Vehicle", command=lambda:return_vehicle(CustID, VID, ReturnDate))
    return_btn.grid(row = 2, column = 0, columnspan = 3, padx = 100)

    conn.commit()
    conn.close()

def return_vehicle(CustID, VID, ReturnDate):
    reset_root()

    conn = sqlite3.connect('car_rental.db')
    c = conn.cursor()

    c.execute("""
    SELECT PaymentDate
    FROM Rental
    WHERE CustID = ? AND VehicleID = ? AND ReturnDate = ?""", (
    CustID, VID, ReturnDate))

    rental_info = c.fetchall()
    if (rental_info[0][0] == 'NULL'):
        payment_date = date.today()
    else:
        payment_date = rental_info[0][0]

    c.execute("""
        UPDATE RENTAL
        SET Returned = 1, PaymentDate = ?
        WHERE CustID = ? AND VehicleID = ? AND ReturnDate = ?""",
    (payment_date, CustID, VID, ReturnDate))

    conn.commit()
    conn.close()
    pick_option()

def view_balance():
    reset_root()

    customer_name_label = Label(root, text = 'Customer Name: ')
    customer_name_label.grid(row = 0, column=0)
    CustomerName = Entry(root, width = 30)
    CustomerName.grid(row=0, column = 1, padx = 20)

    customer_id_label = Label(root, text = 'Customer ID: ')
    customer_id_label.grid(row =1, column = 0)
    CustomerID = Entry(root, width = 30)
    CustomerID.grid(row=1, column = 1, padx = 20)

    view_btn = Button(root, text = 'View', command=lambda: show_balance( CustomerName.get(), CustomerID.get()))
    view_btn.grid(row = 2, column = 0, columnspan = 3, padx= 100, ipadx = 140)

    home_btn = Button(root, text = 'Home', command = pick_option)
    home_btn.grid(row = 3, column = 0, columnspan = 3, padx= 100, ipadx = 140)

def show_balance(name, id):
    reset_root()

    conn = sqlite3.connect('car_rental.db')
    c = conn.cursor()

    if len(id) > 0:
        c.execute("""
            SELECT CustID, Name, CASE WHEN RentalBalance is NULL THEN 0 ELSE SUM(RentalBalance) END AS TotalBalance
            FROM Customer LEFT OUTER JOIN vRentalInfo on CustID = CustomerID
            WHERE CustID = ?
            GROUP BY CustID
            ORDER BY SUM(RentalBalance) DESC""",
        (id,))
    elif len(name) > 0:
        c.execute("""
            SELECT CustID, Name, CASE WHEN RentalBalance is NULL THEN 0 ELSE SUM(RentalBalance) END AS TotalBalance
            FROM Customer LEFT OUTER JOIN vRentalInfo on CustID = CustomerID
            WHERE Name LIKE ?
            GROUP BY CustID
            ORDER BY SUM(RentalBalance) DESC""",
        ("%"+name+"%",))
    else:
        c.execute("""
            SELECT CustID, Name, CASE WHEN RentalBalance is NULL THEN 0 ELSE SUM(RentalBalance) END AS TotalBalance
            FROM Customer LEFT OUTER JOIN vRentalInfo on CustID = CustomerID
            GROUP BY CustID
            ORDER BY SUM(RentalBalance) DESC""")

    rental_info = c.fetchall()
    display_info = "CustomerID | CustomerName | Balance Due\n"
    for rental in rental_info:
        display_info += str(rental[0]) + " | " + rental[1] + " | " + str(rental[2]) + '\n'

    info_label = Label(root, text = display_info)
    info_label.grid(row = 0, pady = 10, padx = 100)

    home_btn = Button(root, text = 'Home', command = pick_option)
    home_btn.grid(row = 4, column = 0, columnspan = 3, padx= 100)


def create_view():
    conn = sqlite3.connect('car_rental.db')
    c = conn.cursor()

    c.execute("""
        DROP VIEW IF EXISTS vRentalInfo
    """)

    c.execute("""
        CREATE VIEW vRentalInfo AS
        SELECT OrderDate, StartDate, ReturnDate, RentalType * Qty as TotalDays, VehicleID as VIN,
            Description as Vehicle,
            CASE Type
                WHEN 1 THEN 'Compact'
                WHEN 2 THEN 'Medium'
                WHEN 3 THEN 'Large'
                WHEN 4 THEN 'SUV'
                WHEN 5 THEN 'Truck'
                WHEN 6 THEN 'VAN'
            END Type,
            CASE Category
                WHEN 0 THEN 'Basic'
                WHEN 1 THEN 'Luxury'
            END Category,
            CustID as CustomerID, Name as CustomerName, TotalAmount as OrderAmount,
            CASE PaymentDate
                WHEN 'NULL' THEN TotalAmount
                ELSE 0
            END RentalBalance
        FROM CUSTOMER NATURAL JOIN RENTAL NATURAL JOIN VEHICLE NATURAL JOIN RATE
        ORDER BY StartDate
    """)

    conn.commit()
    conn.close()

def create_returned_col():
    conn = sqlite3.connect('car_rental.db')
    c = conn.cursor()

    c.execute("""ALTER TABLE RENTAL ADD Returned INT""")
    c.execute("""
        UPDATE RENTAL
        SET Returned = CASE PaymentDate
        WHEN 'NULL' THEN 0
        ELSE 1
        END
    """)

    conn.commit()
    conn.close()

#this function is to create 3 button: add new customer, new car, and reserve a rental
def pick_option():
    reset_root()

    myFont = font.Font(family='Helvetica', size=30, weight='bold')
    welcome_font = font.Font(family='Comic Sans MS', size = 20)

    welcome = Label(root, text = "Welcome to car rental system")
    welcome['font'] = welcome_font
    welcome.grid(row = 0, column = 0, padx = 100)

    add_cust_btn = Button(root, text = 'Add New Customer', command = add_new_cust)
    add_cust_btn['font'] = myFont
    add_cust_btn.grid(row = 1, column = 0, columnspan = 3, padx= 100, pady = (100,0))

    add_car_btn = Button(root, text = 'Add New Vehicle', command = add_new_car)
    add_car_btn['font'] = myFont
    add_car_btn.grid(row = 2, column = 0, columnspan = 3, padx= 100)

    add_rental_btn = Button(root, text = 'Reserve a Vehicle', command = add_new_rental)
    add_rental_btn['font'] = myFont
    add_rental_btn.grid(row = 3, column = 0, columnspan = 3, padx= 100)

    return_car_btn = Button(root, text = 'Return Vehicle', command = return_car)
    return_car_btn['font'] = myFont
    return_car_btn.grid(row = 4, column = 0, columnspan = 3, padx= 100)

    view_balance_btn = Button(root, text = 'View Balance', command = view_balance)
    view_balance_btn['font'] = myFont
    view_balance_btn.grid(row = 5, column = 0, columnspan = 3, padx= 100)

#execute my window, main function
create_db()
create_returned_col()
create_view()
pick_option()
win.mainloop()
