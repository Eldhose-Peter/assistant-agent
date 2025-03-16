import sqlite3
import os

# Create a new SQLite database
db_name = 'sales_order.sqlite'

# Remove the database if it already exists
if os.path.exists(db_name):
    os.remove(db_name)

# Connect to the database (this will create it if it doesn't exist)
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Read schema SQL from file (alternatively, you can embed it here)
schema_sql = '''
-- Create tables for SalesOrderSchema
CREATE TABLE Customer (
    CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    Email VARCHAR(255),
    Phone VARCHAR(20),
    BillingAddress TEXT,
    ShippingAddress TEXT,
    CustomerSince DATE,
    IsActive BOOLEAN
);

CREATE TABLE SalesOrder (
    SalesOrderID INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerID INTEGER,
    OrderDate DATE,
    RequiredDate DATE,
    ShippedDate DATE,
    Status VARCHAR(50),
    Comments TEXT,
    PaymentMethod VARCHAR(50),
    IsPaid BOOLEAN,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

CREATE TABLE Product (
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductName VARCHAR(255),
    Description TEXT,
    UnitPrice DECIMAL(10, 2),
    StockQuantity INTEGER,
    ReorderLevel INTEGER,
    Discontinued BOOLEAN
);

CREATE TABLE LineItem (
    LineItemID INTEGER PRIMARY KEY AUTOINCREMENT,
    SalesOrderID INTEGER,
    ProductID INTEGER,
    Quantity INTEGER,
    UnitPrice DECIMAL(10, 2),
    Discount DECIMAL(10, 2),
    TotalPrice DECIMAL(10, 2),
    FOREIGN KEY (SalesOrderID) REFERENCES SalesOrder(SalesOrderID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

CREATE TABLE Employee (
    EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    Email VARCHAR(255),
    Phone VARCHAR(20),
    HireDate DATE,
    Position VARCHAR(100),
    Salary DECIMAL(10, 2)
);

CREATE TABLE Supplier (
    SupplierID INTEGER PRIMARY KEY AUTOINCREMENT,
    CompanyName VARCHAR(255),
    ContactName VARCHAR(100),
    ContactTitle VARCHAR(50),
    Address TEXT,
    Phone VARCHAR(20),
    Email VARCHAR(255)
);

CREATE TABLE InventoryLog (
    LogID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductID INTEGER,
    ChangeDate DATE,
    QuantityChange INTEGER,
    Notes TEXT,
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
'''

# Execute schema creation
cursor.executescript(schema_sql)

# Read sample data SQL
data_sql = '''
-- Insert sample data into Customer table
INSERT INTO Customer (FirstName, LastName, Email, Phone, BillingAddress, ShippingAddress, CustomerSince, IsActive)
VALUES
    ('John', 'Smith', 'john.smith@email.com', '555-123-4567', '123 Main St, Anytown, USA', '123 Main St, Anytown, USA', '2020-01-15', 1),
    ('Emma', 'Johnson', 'emma.j@email.com', '555-234-5678', '456 Oak Ave, Somewhere, USA', '456 Oak Ave, Somewhere, USA', '2020-03-22', 1),
    ('Michael', 'Brown', 'michael.b@email.com', '555-345-6789', '789 Pine Rd, Nowhere, USA', '789 Pine Rd, Nowhere, USA', '2021-02-10', 1),
    ('Sophia', 'Davis', 'sophia.d@email.com', '555-456-7890', '321 Elm St, Anywhere, USA', '321 Elm St, Anywhere, USA', '2021-05-18', 1),
    ('William', 'Wilson', 'will.w@email.com', '555-567-8901', '654 Maple Dr, Someplace, USA', '654 Maple Dr, Someplace, USA', '2021-07-30', 0);

-- Insert sample data into Product table
INSERT INTO Product (ProductName, Description, UnitPrice, StockQuantity, ReorderLevel, Discontinued)
VALUES
    ('Laptop Pro X', 'High-performance laptop with 16GB RAM and 512GB SSD', 1299.99, 25, 5, 0),
    ('Smartphone Y', 'Latest smartphone with 128GB storage and dual camera', 799.99, 50, 10, 0),
    ('Wireless Headphones', 'Noise-cancelling wireless headphones with 30-hour battery life', 199.99, 100, 15, 0),
    ('Smart Watch', 'Fitness tracker and smartwatch with heart rate monitor', 249.99, 30, 8, 0),
    ('Tablet Z', '10-inch tablet with 64GB storage and stylus support', 349.99, 20, 5, 0),
    ('Desk Chair', 'Ergonomic office chair with lumbar support', 149.99, 15, 3, 0),
    ('Coffee Maker', 'Programmable coffee maker with thermal carafe', 79.99, 40, 10, 0),
    ('Bluetooth Speaker', 'Portable waterproof Bluetooth speaker', 59.99, 75, 15, 0),
    ('External Hard Drive', '2TB portable external hard drive', 89.99, 35, 7, 0),
    ('Gaming Mouse', 'High-precision gaming mouse with customizable buttons', 49.99, 60, 12, 1);

-- Insert sample data into Employee table
INSERT INTO Employee (FirstName, LastName, Email, Phone, HireDate, Position, Salary)
VALUES
    ('James', 'Anderson', 'james.a@company.com', '555-111-2222', '2019-03-10', 'Sales Manager', 75000.00),
    ('Lisa', 'Taylor', 'lisa.t@company.com', '555-222-3333', '2019-06-15', 'Sales Representative', 45000.00),
    ('Robert', 'Martinez', 'robert.m@company.com', '555-333-4444', '2020-02-20', 'Sales Representative', 42000.00),
    ('Emily', 'Garcia', 'emily.g@company.com', '555-444-5555', '2020-09-05', 'Customer Service', 38000.00),
    ('David', 'Lee', 'david.l@company.com', '555-555-6666', '2021-01-12', 'Warehouse Manager', 52000.00);

-- Insert sample data into Supplier table
INSERT INTO Supplier (CompanyName, ContactName, ContactTitle, Address, Phone, Email)
VALUES
    ('Tech Innovations Inc.', 'Thomas Wilson', 'Sales Director', '789 Industry Pkwy, Tech City, USA', '555-777-8888', 'sales@techinnovations.com'),
    ('Global Electronics', 'Maria Rodriguez', 'Account Manager', '456 Circuit Ave, Electro City, USA', '555-888-9999', 'accounts@globalelectronics.com'),
    ('Office Solutions', 'Daniel Johnson', 'CEO', '123 Business Blvd, Commerce Town, USA', '555-999-0000', 'djohnson@officesolutions.com'),
    ('Home Appliances Ltd.', 'Sarah Brown', 'Sales Representative', '321 Appliance St, Home City, USA', '555-000-1111', 'sales@homeappliances.com'),
    ('Gaming Gear Co.', 'Kevin Phillips', 'Marketing Director', '654 Gamer Way, Game City, USA', '555-111-2222', 'kphillips@gaminggear.com');

-- Insert sample data into SalesOrder table
INSERT INTO SalesOrder (CustomerID, OrderDate, RequiredDate, ShippedDate, Status, Comments, PaymentMethod, IsPaid)
VALUES
    (1, '2022-01-15', '2022-01-20', '2022-01-18', 'Delivered', 'Customer requested gift wrapping', 'Credit Card', 1),
    (2, '2022-02-03', '2022-02-08', '2022-02-07', 'Delivered', NULL, 'PayPal', 1),
    (3, '2022-03-10', '2022-03-15', '2022-03-12', 'Delivered', 'Fragile items', 'Credit Card', 1),
    (4, '2022-04-05', '2022-04-10', '2022-04-08', 'Delivered', NULL, 'Credit Card', 1),
    (5, '2022-05-20', '2022-05-25', NULL, 'Processing', 'Customer requested expedited shipping', 'Bank Transfer', 0),
    (1, '2022-06-12', '2022-06-17', '2022-06-15', 'Delivered', NULL, 'Credit Card', 1),
    (2, '2022-07-08', '2022-07-13', '2022-07-10', 'Delivered', NULL, 'PayPal', 1),
    (3, '2022-08-25', '2022-08-30', NULL, 'Cancelled', 'Customer cancelled order', 'Credit Card', 0);

-- Insert sample data into LineItem table
INSERT INTO LineItem (SalesOrderID, ProductID, Quantity, UnitPrice, Discount, TotalPrice)
VALUES
    (1, 1, 1, 1299.99, 0.00, 1299.99),
    (1, 3, 1, 199.99, 10.00, 189.99),
    (2, 2, 1, 799.99, 0.00, 799.99),
    (2, 4, 1, 249.99, 0.00, 249.99),
    (3, 5, 1, 349.99, 15.00, 334.99),
    (3, 8, 2, 59.99, 0.00, 119.98),
    (4, 6, 1, 149.99, 0.00, 149.99),
    (4, 7, 1, 79.99, 0.00, 79.99),
    (5, 9, 2, 89.99, 5.00, 170.98),
    (6, 2, 1, 799.99, 50.00, 749.99),
    (7, 3, 2, 199.99, 20.00, 359.98),
    (7, 8, 1, 59.99, 0.00, 59.99),
    (8, 1, 1, 1299.99, 0.00, 1299.99);

-- Insert sample data into InventoryLog table
INSERT INTO InventoryLog (ProductID, ChangeDate, QuantityChange, Notes)
VALUES
    (1, '2022-01-10', 30, 'Initial stock'),
    (2, '2022-01-10', 60, 'Initial stock'),
    (3, '2022-01-10', 120, 'Initial stock'),
    (1, '2022-01-18', -1, 'Order #1'),
    (3, '2022-01-18', -1, 'Order #1'),
    (2, '2022-02-07', -1, 'Order #2'),
    (4, '2022-02-07', -1, 'Order #2'),
    (1, '2022-02-15', 10, 'Restocking'),
    (5, '2022-03-12', -1, 'Order #3'),
    (8, '2022-03-12', -2, 'Order #3'),
    (6, '2022-04-08', -1, 'Order #4'),
    (7, '2022-04-08', -1, 'Order #4'),
    (2, '2022-06-15', -1, 'Order #6'),
    (3, '2022-07-10', -2, 'Order #7'),
    (8, '2022-07-10', -1, 'Order #7');
'''

# Execute data insertion
cursor.executescript(data_sql)

# Commit changes and close connection
conn.commit()
conn.close()

print(f"Database '{db_name}' created successfully with sample data.")