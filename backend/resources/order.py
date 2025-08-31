from flask_restful import Resource
from db_connection import query_db


class OrderResource(Resource):
    def get(self, order_id):
        order = query_db(
            "SELECT * FROM orders WHERE order_id = ?", (order_id,), one=True
        )
        if not order:
            return {"error": "Order not found"}, 404

        items = query_db(
            """
            SELECT p.name, p.brand, oi.quantity, oi.price
            FROM order_items oi JOIN products p ON oi.product_id = p.product_id
            WHERE oi.order_id = ?""",
            (order_id,),
        )
        return {"order": dict(order), "items": [dict(i) for i in items]}
