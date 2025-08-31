import sqlite3
import uuid
import datetime

conn = sqlite3.connect("virtual_cart.db")
cursor = conn.cursor()

# Drop existing tables if any
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
    cart_id TEXT PRIMARY KEY,
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
    stock INTEGER DEFAULT 0,
    image_url TEXT,
    class TEXT,
    discount REAL DEFAULT 0.0,
    description TEXT,
    created_at TEXT,
    updated_at TEXT
)
"""
)

cursor.execute(
    """
CREATE TABLE cart_items (
    cart_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id TEXT NOT NULL,
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
    cart_id TEXT NOT NULL,
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

# Insert sample products with new fields
now = datetime.datetime.now().isoformat()
products = [
    (
        "123456789012",
        "Milk 1L",
        "DairyBest",
        60.0,
        50,
        "https://images.unsplash.com/photo-1585238342029-4e84f9a56b6f",
        "Dairy",
        5.0,
        "Fresh 1L milk pack",
        now,
        now,
    ),
    (
        "321654987654",
        "Whole Wheat Bread",
        "BakeHouse",
        45.0,
        30,
        "https://images.unsplash.com/photo-1608198093002-ad4e005484b7",
        "Bakery",
        0.0,
        "Healthy wheat bread",
        now,
        now,
    ),
    (
        "543216789012",
        "Shampoo",
        "HairGlow",
        120.5,
        25,
        "https://images.unsplash.com/photo-1583259033943-3b8a148d464d",
        "Personal Care",
        10.0,
        "Anti-dandruff shampoo",
        now,
        now,
    ),
    (
        "789123456098",
        "Eggs 12 pack",
        "FarmFresh",
        85.0,
        40,
        "https://images.unsplash.com/photo-1589927986089-35812388d1f4",
        "Dairy",
        0.0,
        "Farm fresh eggs",
        now,
        now,
    ),
    (
        "234567890123",
        "Chips",
        "Snackers",
        25.5,
        100,
        "https://images.unsplash.com/photo-1585238341970-2f24e0d83c31",
        "Snacks",
        15.0,
        "Potato chips family pack",
        now,
        now,
    ),
    (
        "111222333444",
        "Toothpaste",
        "WhiteSmile",
        55.0,
        60,
        "https://upload.wikimedia.org/wikipedia/commons/5/5c/ColgateToothpaste.jpg",
        "Personal Care",
        0.0,
        "Mint flavor toothpaste",
        now,
        now,
    ),
]
cursor.executemany(
    """
    INSERT INTO products 
    (barcode, name, brand, price, stock, image_url, class, discount, description, created_at, updated_at) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    products,
)

# Insert a dummy cart with UUID
cart_id = str(uuid.uuid1())
cursor.execute(
    "INSERT INTO carts (cart_id, created_at, is_active, device_id) VALUES (?, ?, ?, ?)",
    (cart_id, now, 1, "cartdev-01"),
)

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

print("✅ Virtual Cart DB updated with new product fields and dummy data")
