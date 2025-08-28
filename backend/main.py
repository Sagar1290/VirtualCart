from flask import Flask, jsonify, request, send_from_directory
from datetime import datetime
import sqlite3
from flask_cors import CORS


app = Flask(__name__, static_folder="../frontend/build", static_url_path='')
CORS(app)
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


@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/product/<barcode>", methods=["GET"])
def get_product(barcode):
    product = query_db("SELECT * FROM products WHERE barcode = ?", [barcode], one=True)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(dict(product))


@app.route("/cart", methods=["POST"])
def create_cart():
    device_id = request.json.get("device_id")
    if not device_id:
        return jsonify({"error": "device_id required"}), 400
    created_at = datetime.now().isoformat()
    query_db(
        "INSERT INTO carts (created_at, is_active, device_id) VALUES (?, 1, ?)",
        (created_at, device_id),
        commit=True,
    )
    cart_id = query_db("SELECT last_insert_rowid()", one=True)[0]
    return jsonify({"cart_id": 10})


@app.route("/cart/<int:cart_id>/add", methods=["POST"])
def add_to_cart(cart_id):
    barcode = request.json.get("barcode")
    quantity = request.json.get("quantity", 1)
    if not barcode:
        return jsonify({"error": "barcode required"}), 400
    product = query_db(
        "SELECT product_id, price FROM products WHERE barcode = ?", [barcode], one=True
    )
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    now = datetime.now().isoformat()

    # Check if cart item exists to update quantity
    existing = query_db(
        "SELECT cart_item_id, quantity FROM cart_items WHERE cart_id = ? AND product_id = ?",
        (cart_id, product["product_id"]),
        one=True,
    )
    if existing:
        new_qty = existing["quantity"] + quantity
        query_db(
            "UPDATE cart_items SET quantity = ?, added_at = ? WHERE cart_item_id = ?",
            (new_qty, now, existing["cart_item_id"]),
            commit=True,
        )
    else:
        query_db(
            "INSERT INTO cart_items (cart_id, product_id, quantity, added_at) VALUES (?, ?, ?, ?)",
            (cart_id, product["product_id"], quantity, now),
            commit=True,
        )

    return jsonify({"message": "Product added to cart"})


@app.route("/cart/<int:cart_id>", methods=["GET"])
def view_cart(cart_id):
    items = query_db(
        """
        SELECT p.name, p.brand, p.price, ci.quantity 
        FROM cart_items ci JOIN products p ON ci.product_id = p.product_id 
        WHERE ci.cart_id = ?""",
        [cart_id],
    )
    if not items:
        return jsonify({"error": "Cart empty or not found"}), 404
    cart_items = []
    total = 0
    for i in items:
        total += i["price"] * i["quantity"]
        cart_items.append(dict(i))
    return jsonify({"items": cart_items, "total_price": total})


@app.route("/cart/<int:cart_id>/checkout", methods=["POST"])
def checkout(cart_id):
    # Calculate total price
    items = query_db(
        """
        SELECT p.product_id, p.price, ci.quantity 
        FROM cart_items ci JOIN products p ON ci.product_id = p.product_id 
        WHERE ci.cart_id = ?""",
        [cart_id],
    )
    if not items:
        return jsonify({"error": "Cart empty or not found"}), 404
    total_price = sum(i["price"] * i["quantity"] for i in items)
    status = "Paid"
    created_at = datetime.now().isoformat()

    # Create order
    query_db(
        "INSERT INTO orders (cart_id, order_total, status, created_at) VALUES (?, ?, ?, ?)",
        (cart_id, total_price, status, created_at),
        commit=True,
    )
    order_id = query_db("SELECT last_insert_rowid()", one=True)[0]

    # Insert order items
    for i in items:
        query_db(
            "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
            (order_id, i["product_id"], i["quantity"], i["price"]),
            commit=True,
        )

    # Deactivate cart
    query_db(
        "UPDATE carts SET is_active = 0 WHERE cart_id = ?", (cart_id,), commit=True
    )

    # Dummy payment record (expand as needed)
    query_db(
        "INSERT INTO payments (order_id, amount, payment_status, method) VALUES (?, ?, ?, ?)",
        (order_id, total_price, "Completed", "UPI"),
        commit=True,
    )

    return jsonify(
        {
            "message": "Checkout successful",
            "order_id": order_id,
            "total_price": total_price,
        }
    )


@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = query_db("SELECT * FROM orders WHERE order_id = ?", (order_id,), one=True)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    items = query_db(
        """
        SELECT p.name, p.brand, oi.quantity, oi.price
        FROM order_items oi JOIN products p ON oi.product_id = p.product_id
        WHERE oi.order_id = ?""",
        (order_id,),
    )
    return jsonify({"order": dict(order), "items": [dict(i) for i in items]})


if __name__ == "__main__":
    app.run(debug=True)
