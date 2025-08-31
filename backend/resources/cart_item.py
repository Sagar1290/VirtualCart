from flask_restful import Resource
from db_connection import query_db
from flask import request
from datetime import datetime


class CartItemResource(Resource):
    def post(self, cart_id):
        barcode = request.json.get("barcode")
        quantity = request.json.get("quantity", 1)

        if not barcode:
            return {"error": "barcode required"}, 400
        product = query_db(
            "SELECT product_id, price, discount FROM products WHERE barcode = ?",
            [barcode],
            one=True,
        )

        if product is None:
            return {"error": "Product not found"}, 404

        now = datetime.now().isoformat()
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

        return {"message": "Product added to cart"}

    def get(self, cart_id):
        items = query_db(
            """
            SELECT p.barcode, p.name, p.brand, p.price, p.discount, ci.quantity 
            FROM cart_items ci 
            JOIN products p ON ci.product_id = p.product_id 
            WHERE ci.cart_id = ?
            """,
            [cart_id],
        )
        if not items:
            return {"error": "Cart empty or not found"}, 404

        cart_items = []

        for i in items:
            cart_items.append(dict(i))

        return {"items": cart_items}

    def delete(self, cart_id):
        barcode = request.json.get("barcode")
        if not barcode:
            return {"error": "barcode required"}, 400

        product = query_db(
            "SELECT product_id FROM products WHERE barcode = ?",
            [barcode],
            one=True,
        )
        if product is None:
            return {"error": "Product not found"}, 404

        query_db(
            "DELETE FROM cart_items WHERE cart_id = ? AND product_id = ?",
            (cart_id, product["product_id"]),
            commit=True,
        )

        return {"message": "Product removed from cart"}
