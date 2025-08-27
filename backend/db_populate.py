import sqlite3

conn = sqlite3.connect("virtual_cart.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS payments")
cursor.execute("DROP TABLE IF EXISTS order_items")
cursor.execute("DROP TABLE IF EXISTS orders")
cursor.execute("DROP TABLE IF EXISTS cart_items")
cursor.execute("DROP TABLE IF EXISTS carts")
cursor.execute("DROP TABLE IF EXISTS products")

# Create tables
cursor.execute(
    """
CREATE TABLE carts (
    cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    device_id TEXT
)
"""
)
cursor.execute(
    """
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    barcode TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    brand TEXT,
    price REAL NOT NULL,
    stock INTEGER DEFAULT 0
)
"""
)
cursor.execute(
    """
CREATE TABLE cart_items (
    cart_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER DEFAULT 1,
    added_at TEXT,
    FOREIGN KEY (cart_id) REFERENCES carts(cart_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
"""
)
cursor.execute(
    """
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INTEGER NOT NULL,
    order_total REAL,
    status TEXT,
    created_at TEXT,
    FOREIGN KEY (cart_id) REFERENCES carts(cart_id)
)
"""
)
cursor.execute(
    """
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER DEFAULT 1,
    price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
"""
)
cursor.execute(
    """
CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    amount REAL,
    payment_status TEXT,
    method TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
)
"""
)

products = [
    ("123456789012", "Milk 1L", "DairyBest", 60.0, 50),
    ("321654987654", "Whole Wheat Bread", "BakeHouse", 45.0, 30),
    ("543216789012", "Shampoo", "HairGlow", 120.5, 25),
    ("789123456098", "Eggs 12 pack", "FarmFresh", 85.0, 40),
    ("234567890123", "Chips", "Snackers", 25.5, 100),
    ("111222333444", "Toothpaste", "WhiteSmile", 55.0, 60),
]
cursor.executemany(
    "INSERT INTO products (barcode, name, brand, price, stock) VALUES (?, ?, ?, ?, ?)",
    products,
)

# Insert a dummy cart
import datetime

now = datetime.datetime.now().isoformat()
cursor.execute(
    "INSERT INTO carts (created_at, is_active, device_id) VALUES (?, ?, ?)",
    (now, 1, "cartdev-01"),
)
cart_id = cursor.lastrowid

# Insert dummy cart items
cursor.execute(
    "INSERT INTO cart_items (cart_id, product_id, quantity, added_at) VALUES (?, ?, ?, ?)",
    (cart_id, 1, 2, now),
)  # Milk
cursor.execute(
    "INSERT INTO cart_items (cart_id, product_id, quantity, added_at) VALUES (?, ?, ?, ?)",
    (cart_id, 2, 1, now),
)  # Bread

# Insert dummy order
order_total = 2 * 60.0 + 1 * 45.0  # Milk + Bread
cursor.execute(
    "INSERT INTO orders (cart_id, order_total, status, created_at) VALUES (?, ?, ?, ?)",
    (cart_id, order_total, "Paid", now),
)
order_id = cursor.lastrowid

# Insert dummy order items
cursor.execute(
    "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
    (order_id, 1, 2, 60.0),
)
cursor.execute(
    "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
    (order_id, 2, 1, 45.0),
)

# Insert dummy payment
cursor.execute(
    "INSERT INTO payments (order_id, amount, payment_status, method) VALUES (?, ?, ?, ?)",
    (order_id, order_total, "Completed", "UPI"),
)

conn.commit()
conn.close()

"Virtual Cart DB with schema and dummy data created as virtual_cart.db"
