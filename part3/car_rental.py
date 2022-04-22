from hmac import new
from tkinter import *
from tkinter import ttk
import sqlite3, csv
import tkinter.font as font
import types
import pandas as pd

#create tkinter window
win = Tk()
win.geometry("500x500")
win.title('CAR RENTAL')
root = Frame(win)
root.pack(side="top", expand=True, fill="both")

def reset_root():
    for widgets in root.winfo_children():
          widgets.destroy()

#this function is to create the database schema and imort data from CSV files
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
        Weekly INTEGER NOT NULL,
        Daily INTEGER NOT NULL,

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
    df = pd.read_csv("RENTAL.csv")
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

def add_new_rental():
    reset_root()

    name_label = Label(root, text = 'name: ')
    name_label.grid(row =0, column = 0)
    name = Entry(root, width = 30)
    name.grid(row=0, column = 1, padx = 20)
    
    phone_label = Label(root, text = 'phone: ')
    name_label.grid(row =1, column = 0)
    phone = Entry(root, width = 30)
    phone.grid(row = 1, column = 1, padx = 20)

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


#execute my window, main function
create_db()
pick_option()
win.mainloop()
