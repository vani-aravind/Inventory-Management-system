#   Inventory Management System

  ## Description:
Here,Inventory Management System is designed to manage product inventory efficiently. It allows users to view,update(add/delete) products while tracking stock quantity and prices. The system is designed using Python3.14.0 
## Objectives:
 Here Inventory Management System tracks:\
 • Products which in stock\
 • Suppliers who provide the products\
 • Purchases: stock coming in\
 • Sales: stock going out\
 • Users who operate the system
 
 ## Requirements:
  •User registration/login as admin/staff: Only loggined userscan perform inventory operations\
  •Add new products to inventory\
  •View all available products and current inventory\
  •Update inventory after purchase\
  •Update inventory after sales\
  •Only loggedin as admin can add additional users
  
 ## Technology Stack:
 •Operating System: Windows\
 •Programming Language: Python 3.14.0\
 •Database: SQLite (built-in with Python)

## Database Schema
 ### 1. Database Used: SQLite database (inventorymanagement.db)
 ### 2.Table Structure

### Table: Users
|Field Name|	Data Type|	
|------------| ---------| 
|user_id| INTEGER PRIMARY KEY AUTOINCREMENT|
|user_name| VARCHAR(20) UNIQUE|
|password |TEXT|
|role VARCHAR(20)|
|email_id VARCHAR(100))|

### Table:Products
|Field Name|	Data Type|	
|------------| ---------| 
|product_id|	INTEGER (Primary Key)	Unique product ID|
|product_name|	VARCHAR(20) NOT NULL|
|category| VARCHAR(50)|
|unit_price|DECIMAL(10,2) NOT NULL|
|quantity_instoke|	INTEGER DEFAULT 0	|
|created_at|TIMESTAMP DEFAULT CURRENT_TIMESTAMP|	

### Table: Suppliers
|Field Name|	Data Type|	
|------------| ---------| 
|supplier_id| INTEGER PRIMARY KEY AUTOINCREMENT|
|supplier_name| VARCHAR(20) NOT NULL|
|phone_no |VARCHAR(20)|
|email_id |VARCHAR(100)|
|address| TEXT|

### Table: Purchases
|Field Name|	Data Type|	
|------------| ---------| 
|purchase_id| INTEGER PRIMARY KEY AUTOINCREMENT|
|product_id| INTEGER NOT NULL|
|supplier_id| INTEGER NOT NULL|
|user_id| INTEGER NOT NULL|
|quantity| INTEGER NOT NULL|
|purchase_price| DECIMAL(10,2)|
|purchase_date| DATE DEFAULT CURRENT_DATE|   

### Table:Sales
|Field Name|	Data Type|	
|------------| ---------| 
|sale_id INTEGER| PRIMARY KEY AUTOINCREMENT|
|product_id| INTEGER NOT NULL|
|user_id| INTEGER NOT NULL           
|quantity |INTEGER NOT NULL|            
|sale_price| DECIMAL(10,2)|            
|sale_date |DATE DEFAULT CURRENT_DATE|              

##  System Flow
1.Start the program\
2. User registration/login\
3.Select options from the menu:\
   •Add Products\
   •Add Suppliers\
   •View Products\
   •Add Purchase\
   •Add Sales\
   •Exit\
4. required details as prompted\
5.Data is automatically saved in the database
