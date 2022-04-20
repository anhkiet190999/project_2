from hmac import new
from tkinter import *
import sqlite3
import tkinter.font as font
from numpy import size

#create tkinter window
win = Tk()
win.geometry("500x500")
win.title('CAR RENTAL')
root = Frame(win)
root.pack(side="top", expand=True, fill="both")

def reset_root():
    for widgets in root.winfo_children():
          widgets.destroy()

#this function is to create the database schema
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
        PaymentDate DATE NOT NULL,

        CONSTRAINT PK_Rental PRIMARY KEY (CustID, VehicleID, StartDate),

        FOREIGN KEY (CustID) REFERENCES CUSTOMER (CustID)
        ON DELETE CASCADE ON UPDATE CASCADE

        FOREIGN KEY (VehicleID) REFERENCES VEHICLE (VehicleID)
        ON DELETE CASCADE ON UPDATE CASCADE
    )
    ''')
    print("created tables successfuly!")
    #commint changes and close cursor
    conn.commit()
    conn.close()

def add_new_cust():
    reset_root()

    name_label = Label(root, text = 'name: ')
    name_label.grid(row = 0, column = 0, padx = (100,0))
    name = Entry(root, width = 30)
    name.grid(row = 0, column = 1, padx = 20)
    
    phone_label = Label(root, text = 'phone: ')
    phone_label.grid(row =1, column = 0, padx = (100,0))
    phone = Entry(root, width = 30)
    phone.grid(row = 1, column = 1, padx = 20)

    submit_btn = Button(root, text = 'Submit', command = add_new_cust)
    submit_btn.grid(row = 2, column = 0, columnspan = 3, padx= 100)

def add_new_car():
    reset_root()

    name_label = Label(root, text = 'name: ')
    name_label.grid(row =0, column = 0)
    name = Entry(root, width = 30)
    name.grid(row=0, column = 1, padx = 20)
    
    phone_label = Label(root, text = 'phone: ')
    name_label.grid(row =1, column = 0)
    phone = Entry(root, width = 30)
    phone.grid(row = 1, column = 1, padx = 20)

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
