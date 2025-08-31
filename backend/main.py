from flask import Flask, send_from_directory
from flask_restful import Api, Resource
from flask_cors import CORS
from resources.cart import CartResource
from resources.product import ProductResource
from resources.order import OrderResource
from resources.cart_item import CartItemResource
from resources.checkout import CheckoutResource

app = Flask(__name__, static_folder="../frontend/build", static_url_path="")
CORS(app)
api = Api(app)


class ServeIndex(Resource):
    def get(self):
        return send_from_directory(app.static_folder, "index.html")


api.add_resource(ServeIndex, "/")
api.add_resource(ProductResource, "/product/<string:barcode>")
api.add_resource(CartResource, "/cart")
api.add_resource(
    CartItemResource,
    "/cart/<string:cart_id>/add",
    "/cart/<string:cart_id>",
    "/cart/<string:cart_id>/delete",
)
api.add_resource(CheckoutResource, "/cart/<string:cart_id>/checkout")
api.add_resource(OrderResource, "/orders/<int:order_id>")


if __name__ == "__main__":
    app.run(debug=True)
