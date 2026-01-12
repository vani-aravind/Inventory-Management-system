# !!!!Mini Project Title: Inventory management System!!!!!

# Objectives:
# Here Inventory Management System tracks:
#• Products which in stock
#• Suppliers who provide the products
#• Purchases: stock coming in
#• Sales: stock going out
#• Users who operate the system


import sqlite3
from datetime import datetime
conn=sqlite3.connect('inventorymanagement.db')
cursor=conn.cursor()

#Table 1: User: Store systen user(admin or staff) and track who made the purchases and sales
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
               user_id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_name VARCHAR(20) UNIQUE,
               password TEXT,
               role VARCHAR(20),
               email_id VARCHAR(100))
''')


# Table 2: Products: Stores products details, stocks increases/decreases based on purchases,sales
#DECIMAL(10,2)- total 10 digits, 2 after decimal point
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name VARCHAR(20) NOT NULL,
            category VARCHAR(50),
            unit_price DECIMAL(10,2) NOT NULL,
            quantity_instock INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
               )

''')

# Table 3: Suppliers: Store supplier information, from where products purchased
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Suppliers(
            supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_name VARCHAR(20) NOT NULL,
            phone_no VARCHAR(20),
            email_id VARCHAR(100),
            address TEXT
            
               )

''')

# Table 3: Purchases: record incoming stock
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Purchases(
            purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            supplier_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            purchase_price DECIMAL(10,2),
            purchase_date DATE DEFAULT CURRENT_DATE,   
            FOREIGN KEY(product_id) REFERENCES Products(product_id),
            FOREIGN KEY(supplier_id) REFERENCES Suppliers(supplier_id),
            FOREIGN KEY(user_id) REFERENCES Users(user_id)
            
               )

''')

# Table 4: Sales: Record sales stocks
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sales(
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            sale_price DECIMAL(10,2),
            sale_date DATE DEFAULT CURRENT_DATE,   
            FOREIGN KEY(product_id) REFERENCES Products(product_id),
            FOREIGN KEY(user_id) REFERENCES Users(user_id)
            
               )

''')

#Add user
def adduser():
    print('!!!!!!!!!!Registration!!!!!!!!!!!')
    user_name=input('Enter user name: ').strip()
    password=input('Enter password: ').strip()
    role=input('Enter the role(admin/staff): ').lower()
    email=input('Enter the email id: ')
    if role not in('admin','staff'):
        print('Invalid role!, User mustbe admin/staff❌')
        return
    try:
        conn=sqlite3.connect('inventorymanagement.db')
        cursor=conn.cursor()
        cursor.execute('''
            INSERT INTO Users(user_name,password,role,email_id)
                VALUES(?,?,?,?)
        ''',(user_name,password,role,email))
        conn.commit()
        print(f'User{user_name} added Successfully✅')
    except sqlite3.IntegrityError:
        print('Username already exists❌')
    conn.close()

# User login
def login():
    print('!!!User Logged in!!!')
    conn=sqlite3.connect('inventorymanagement.db') 
    cursor=conn.cursor()
    user_name=input('Enter user name: ').strip()
    password=input('Enter password: ').strip()
    cursor.execute('''
    SELECT user_id,role FROM Users WHERE user_name=? AND password=?
    ''',(user_name,password))
    result=cursor.fetchone()
    conn.close()
    if result:
        user_id,role=result
        print(f'Logined in successfully! Welcome {user_name}({role})✅')
        return user_id,role
    else:
        print('Invalid username or password❌')
        return None,None

# Add new product to inventory

def addproducts():
    conn=sqlite3.connect('inventorymanagement.db') 
    cursor=conn.cursor()
    pro_name=input('Enter product name: ')
    pro_cate=input('Enter product category: ')
    pro_unit_price=float(input('Enter unit price: '))
    pro_quat_stok=int(input('Enter the quantity in stock: '))
    cursor.execute('''
    INSERT INTO Products(product_name,category,unit_price,quantity_instock )
            VALUES(?,?,?,?)       
''',(pro_name,pro_cate,pro_unit_price,pro_quat_stok))
    conn.commit()
    conn.close()
    print('Product Added✅')

#add values to supplier table
def addsuppliers():
    conn=sqlite3.connect('inventorymanagement.db') 
    cursor=conn.cursor()
    supp_name=input('Enter supplier name: ')
    supp_pho=input('Enter supplier phone number ')
    supp_email=input('Enter supplier email id: ')
    supp_addres=input('Enter supplier address: ')
    cursor.execute('''
    INSERT INTO Suppliers(supplier_name,phone_no,email,address)
            VALUES(?,?,?,?)       
''',(supp_name,supp_pho,supp_email,supp_addres))
    conn.commit()
    conn.close()
    print('Suppliers Added✅')
    
# Update purchase table
def addpurchases(user_id):
    conn=sqlite3.connect('inventorymanagement.db') 
    cursor=conn.cursor()
    pro_id=int(input('Enter product id: '))
    supp_id=int(input('Enter supplier id: '))
    purch_quant=int(input('Enter quantity purchased: '))
    purch_price=float(input('Enter pricefor purchase: '))
    cursor.execute('''
    INSERT INTO Purchases(product_id,supplier_id,user_id,quantity,purchase_price)
            VALUES(?,?,?,?,?)       
''',(pro_id,supp_id,user_id,purch_quant,purch_price))
    conn.commit()

    # Increase inventory after purchase
    cursor.execute('''
    UPDATE Products SET quantity_instock=quantity_instock+? WHERE product_id=?
    ''',(purch_quant,pro_id))
    conn.commit()
    conn.close()
    print('Purchase Added and Stock Updated✅ ')
    
# Update sales
def addsales(user_id):
    conn=sqlite3.connect('inventorymanagement.db') 
    cursor=conn.cursor()
    pro_id=int(input('Enter product id: '))
    sale_quant=int(input('Enter sale quantity: '))
    sale_price=float(input('Enter selling price: '))

    cursor.execute('''
    SELECT quantity_instock FROM Products WHERE product_id=?
    ''',(pro_id,))
    stock=cursor.fetchone()[0]

    # check available stock
    if stock<sale_quant:
        print('No enough stock❌')
        return
    
    cursor.execute('''
    INSERT INTO Sales(product_id,user_id,quantity,sale_price)
            VALUES(?,?,?,?)       
''',(pro_id,user_id,sale_quant,sale_price))
    conn.commit()
   
   # Reduce inventory after sales
    cursor.execute('''
    UPDATE Products SET quantity_instock=quantity_instock-? WHERE product_id=?
    ''',(sale_quant,pro_id))
    conn.commit()
    conn.close()
    print('Sales Added and Stock Updated✅ ')
    
#view all products details
def viewproducts():
    conn=sqlite3.connect('inventorymanagement.db')
    cursor=conn.cursor()
    cursor.execute('''
    SELECT * FROM Products
    ''')
    for row in cursor.fetchall():
        print(row)
    conn.close()

# View current inventory: show product_id,name,instock only
def viewinventory():
    conn=sqlite3.connect('inventorymanagement.db')
    cursor=conn.cursor()
    cursor.execute('''
    SELECT product_id,product_name,quantity_instock FROM Products
    ''')
    alldata=cursor.fetchall()
    for row in alldata:
        print(row)
    conn.close()


# Allow User to register/login :Only perform oprations after logged in
def welcome():
    print('!!!Welcome to Inventory Management System!!!')
    ch=int(input('enter choice\n1.User Registration\n2.Login'))
    if ch==1:
        adduser()
    elif ch==2:
        user_id,role=login()
        if user_id:
             main(user_id,role)


# Main function
def main(user_id,role):
     
    while True:
        print('Select choice')
        print('1.Add Products\n2.Add Suppliers\n3.Add Purchase\n4.Add Sale\n5.View Products')
        print('6.View Inventory\n7.Add User\n8.Exit')    
        choice=int(input('Enter your choice: '))
        if choice==1:
            addproducts()
        elif choice==2:
            addsuppliers()
        elif choice==3:
            addpurchases(user_id)
        elif choice==4:
            addsales(user_id)
        elif choice==5:
            viewproducts()
        elif choice==6:
           viewinventory()
        elif choice==7:
           if role !='admin':
               print('Only admin can add users❌')
           else:
               adduser()
        elif choice==8:
            print('Exiting...')
            conn.close()
            break
        else:
            print('Invalid choice')

welcome()        