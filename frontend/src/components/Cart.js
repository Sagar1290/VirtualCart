import React from "react";
import { Trash2, Plus, Minus } from "lucide-react";

function Cart({ cartItems, onCheckout, onRemove, onUpdateQty }) {
  const total = cartItems.reduce(
    (sum, item) =>
      sum +
      (item.price - (item.price * (item.discount || 0)) / 100) *
      item.quantity,
    0
  );

  return (
    <div className="border mt-4 p-5 rounded-xl w-[380px] bg-white shadow-md">
      <h4 className="text-lg font-bold mb-3 text-gray-700">🛒 Cart Summary</h4>

      {cartItems.length === 0 ? (
        <p className="text-sm text-gray-500">No items in cart.</p>
      ) : (
        <ul className="divide-y divide-gray-200 mb-3">
          {cartItems.map((item, i) => {
            const discountedPrice =
              item.discount > 0
                ? item.price - (item.price * item.discount) / 100
                : item.price;

            return (
              <li
                key={i}
                className="flex justify-between items-center py-2 text-sm"
              >
                <div>
                  <span className="font-medium">{item.name}</span>{" "}
                  <span className="text-xs text-gray-500">[{item.brand}]</span>
                  <div className="text-xs text-gray-600">
                    ₹{discountedPrice?.toFixed(2)} each
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => onUpdateQty(item, -1)}
                    className="p-1 bg-gray-200 rounded hover:bg-gray-300"
                    disabled={item.quantity <= 1}
                  >
                    <Minus size={14} />
                  </button>
                  <span>{item.quantity}</span>
                  <button
                    onClick={() => onUpdateQty(item, 1)}
                    className="p-1 bg-gray-200 rounded hover:bg-gray-300"
                  >
                    <Plus size={14} />
                  </button>

                  <span className="text-blue-700 font-semibold ml-2">
                    ₹{(discountedPrice * item.quantity).toFixed(2)}
                  </span>

                  <button
                    onClick={() => onRemove(item)}
                    className="ml-2 p-1 bg-red-500 text-white rounded hover:bg-red-600"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              </li>
            );
          })}
        </ul>
      )}

      {cartItems.length > 0 && (
        <>
          <p className="text-right font-bold text-lg text-gray-800">
            Total: ₹{total.toFixed(2)}
          </p>
          <button
            className="mt-3 w-full py-2 bg-purple-600 text-white font-semibold rounded-lg hover:bg-purple-700 transition"
            onClick={onCheckout}
          >
            Checkout
          </button>
        </>
      )}
    </div>
  );
}

export default Cart;
