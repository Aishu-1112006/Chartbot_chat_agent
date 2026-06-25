import sqlite3

conn = sqlite3.connect("sample.db")
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL,
    stock INTEGER
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    customer_id INTEGER,
    quantity INTEGER,
    revenue REAL,
    order_date TEXT
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    city TEXT
);

INSERT OR IGNORE INTO products VALUES
(1,'Laptop','Electronics',999.99,50),
(2,'Phone','Electronics',499.99,100),
(3,'Desk','Furniture',299.99,30),
(4,'Chair','Furniture',199.99,60),
(5,'Headphones','Electronics',149.99,80);

INSERT OR IGNORE INTO customers VALUES
(1,'Alice','alice@email.com','Mumbai'),
(2,'Bob','bob@email.com','Delhi'),
(3,'Charlie','charlie@email.com','Bangalore');

INSERT OR IGNORE INTO orders VALUES
(1,1,1,2,1999.98,'2024-01-15'),
(2,2,2,3,1499.97,'2024-01-16'),
(3,3,1,1,299.99,'2024-02-10'),
(4,4,3,2,399.98,'2024-02-15'),
(5,5,2,5,749.95,'2024-03-01');
""")

conn.commit()
conn.close()
print("Database created successfully!")