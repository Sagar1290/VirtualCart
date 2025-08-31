from flask_restful import Resource
from db_connection import query_db


class ProductResource(Resource):
    def get(self, barcode):
        product = query_db(
            "SELECT * FROM products WHERE barcode = ?", [barcode], one=True
        )
        if product is None:
            return {"error": "Product not found"}, 404

        # Fetch related items of the same class
        related_products = query_db(
            "SELECT * FROM products WHERE class = ? AND barcode != ? LIMIT 5",
            [product["class"], barcode],
        )

        return {
            "product": dict(product),
            "related_products": [dict(rp) for rp in related_products],
        }
