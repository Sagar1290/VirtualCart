from flask_restful import Resource
from db_connection import query_db
from datetime import datetime


class CheckoutResource(Resource):
    def post(self, cart_id):
        items = query_db(
            """
            SELECT p.product_id, p.price, ci.quantity 
            FROM cart_items ci JOIN products p ON ci.product_id = p.product_id 
            WHERE ci.cart_id = ?""",
            [cart_id],
        )
        if not items:
            return {"error": "Cart empty or not found"}, 404

        total_price = sum(i["price"] * i["quantity"] for i in items)
        status = "Paid"
        created_at = datetime.now().isoformat()

        # Insert order
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

        # Mark cart inactive
        query_db(
            "UPDATE carts SET is_active = 0 WHERE cart_id = ?", (cart_id,), commit=True
        )

        # Dummy payment
        query_db(
            "INSERT INTO payments (order_id, amount, payment_status, method) VALUES (?, ?, ?, ?)",
            (order_id, total_price, "Completed", "UPI"),
            commit=True,
        )

        return {
            "message": "Checkout successful",
            "order_id": order_id,
            "total_price": total_price,
        }
