from flask_restful import Resource
from db_connection import query_db
from flask import request
from datetime import datetime
import uuid


class CartResource(Resource):
    def post(self):
        device_id = request.json.get("device_id")
        if not device_id:
            return {"error": "device_id required"}, 400
        created_at = datetime.now().isoformat()
        cart_id = str(uuid.uuid1())
        query_db(
            "INSERT INTO carts (cart_id, created_at, is_active, device_id) VALUES (?, ?, 1, ?)",
            (cart_id, created_at, device_id),
            commit=True,
        )
        return {"cart_id": cart_id}
