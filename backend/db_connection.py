import sqlite3

DB_PATH = "virtual_cart.db"


def query_db(query, args=(), one=False, commit=False):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    if commit:
        conn.commit()
        conn.close()
        return
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv


# from datetime import datetime
# now = datetime.now().isoformat()

# conn = sqlite3.connect("virtual_cart.db")
# cursor = conn.cursor()

# cursor.executemany(
#     """
#     INSERT INTO products
#     (barcode, name, brand, price, stock, image_url, class, discount, description, created_at, updated_at)
#     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#     """,
#     products,
# )
# cursor.execute("ALTER TABLE cart_items ADD COLUMN final_price DECIMAL")
# conn.commit()
