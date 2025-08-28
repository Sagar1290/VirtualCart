import React, { useEffect } from "react";

function Cart({ cartItems, onLoadCart, onCheckout }) {
  useEffect(() => {
    onLoadCart();
  }, []);

  const total = cartItems.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );

  return (
    <div className="border mt-2 p-5 rounded-lg w-[340px] bg-white shadow">
      <h4 className="text-lg font-semibold mb-2">Cart Items</h4>
      {cartItems.length === 0 ? (
        <p className="text-sm text-gray-600">No items in cart.</p>
      ) : (
        <ul className="mb-3">
          {cartItems.map((item, i) => (
            <li key={i} className="flex justify-between py-1">
              <span>
                {item.name}{" "}
                <span className="text-xs text-gray-500">[{item.brand}]</span>
              </span>
              <span>
                x{item.quantity} —{" "}
                <span className="text-blue-700 font-bold">
                  ₹{item.price * item.quantity}
                </span>
              </span>
            </li>
          ))}
        </ul>
      )}
      {cartItems.length > 0 && (
        <>
          <p className="font-bold text-right mb-2">Total: ₹{total}</p>
          <button
            className="px-4 py-1 bg-purple-600 text-white font-semibold rounded hover:bg-purple-700 float-right"
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
