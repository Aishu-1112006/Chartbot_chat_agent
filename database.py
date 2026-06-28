import sqlite3

conn = sqlite3.connect("sample.db")
cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL,
    stock INTEGER
);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    city TEXT
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    customer_id INTEGER,
    quantity INTEGER,
    revenue REAL,
    order_date TEXT
);

INSERT INTO products VALUES
(1,'Laptop','Electronics',999.99,50),
(2,'Phone','Electronics',499.99,100),
(3,'Desk','Furniture',299.99,30),
(4,'Chair','Furniture',199.99,60),
(5,'Headphones','Electronics',149.99,80),
(6,'Monitor','Electronics',399.99,45),
(7,'Keyboard','Electronics',79.99,120),
(8,'Mouse','Electronics',49.99,150),
(9,'Bookshelf','Furniture',249.99,25),
(10,'Lamp','Furniture',89.99,70);

INSERT INTO customers VALUES
(1,'Alice','alice@email.com','Mumbai'),
(2,'Bob','bob@email.com','Delhi'),
(3,'Charlie','charlie@email.com','Bangalore'),
(4,'Diana','diana@email.com','Mumbai'),
(5,'Eve','eve@email.com','Chennai'),
(6,'Frank','frank@email.com','Delhi'),
(7,'Grace','grace@email.com','Hyderabad'),
(8,'Henry','henry@email.com','Bangalore'),
(9,'Iris','iris@email.com','Mumbai'),
(10,'Jack','jack@email.com','Chennai');

INSERT INTO orders VALUES
(1,1,1,2,1999.98,'2025-01-15'),
(2,2,2,3,1499.97,'2025-01-20'),
(3,3,3,1,299.99,'2025-02-10'),
(4,4,4,2,399.98,'2025-02-15'),
(5,5,5,5,749.95,'2025-02-20'),
(6,6,6,1,399.99,'2025-03-01'),
(7,7,7,3,239.97,'2025-03-10'),
(8,8,8,4,199.96,'2025-03-15'),
(9,9,9,1,249.99,'2025-04-01'),
(10,10,10,2,179.98,'2025-04-10'),
(11,1,2,1,999.99,'2025-04-15'),
(12,2,3,2,999.98,'2025-05-01'),
(13,3,4,3,899.97,'2025-05-10'),
(14,4,5,1,199.99,'2025-05-15'),
(15,5,6,2,299.98,'2025-06-01'),
(16,6,7,1,399.99,'2025-06-10'),
(17,7,8,5,399.95,'2025-06-15'),
(18,8,9,2,99.98,'2025-07-01'),
(19,9,10,1,249.99,'2025-07-10'),
(20,10,1,3,269.97,'2025-07-15'),
(21,1,3,1,999.99,'2025-08-01'),
(22,2,4,2,999.98,'2025-08-10'),
(23,3,5,1,299.99,'2025-08-15'),
(24,4,6,4,799.96,'2025-09-01'),
(25,5,7,3,449.97,'2025-09-10'),
(26,6,8,2,799.98,'2025-09-15'),
(27,7,9,1,79.99,'2025-10-01'),
(28,8,10,3,149.97,'2025-10-10'),
(29,9,1,2,499.98,'2025-10-15'),
(30,10,2,1,89.99,'2025-11-01'),
(31,1,4,3,2999.97,'2025-11-10'),
(32,2,5,1,499.99,'2025-11-15'),
(33,3,6,2,599.98,'2025-12-01'),
(34,4,7,1,199.99,'2025-12-10'),
(35,5,8,4,599.96,'2025-12-15'),
(36,6,9,2,799.98,'2026-01-01'),
(37,7,10,3,239.97,'2026-01-10'),
(38,8,1,1,49.99,'2026-01-15'),
(39,9,2,2,499.98,'2026-02-01'),
(40,10,3,1,89.99,'2026-02-10'),
(41,1,5,2,1999.98,'2026-02-15'),
(42,2,6,1,499.99,'2026-03-01'),
(43,3,7,3,899.97,'2026-03-10'),
(44,4,8,2,399.98,'2026-03-15'),
(45,5,9,1,149.99,'2026-04-01'),
(46,6,10,4,1599.96,'2026-04-10'),
(47,7,1,2,159.98,'2026-04-15'),
(48,8,2,5,249.95,'2026-05-01'),
(49,9,3,1,249.99,'2026-05-10'),
(50,10,4,2,179.98,'2026-05-15');
""")

conn.commit()
conn.close()
print("Database created successfully!")