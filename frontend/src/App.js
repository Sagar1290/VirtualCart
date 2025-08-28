import React, { useState, useEffect } from "react";
import Cart from "./components/Cart";
import ProductInfo from "./components/ProductInfo";
import BarcodeInput from "./components/BarcodeInput";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

function App() {
  const [cartId, setCartId] = useState(null);
  const [product, setProduct] = useState(null);
  const [cartItems, setCartItems] = useState([]);
  const [loadingCart, setLoadingCart] = useState(false);
  const [error, setError] = useState(null);

  const createCartSession = async () => {
    setError(null);
    try {
      const res = await fetch(`${API_URL}/cart`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ device_id: "frontend-cart-01" }),
      });
      if (!res.ok) throw new Error("Failed to create cart");
      const data = await res.json();
      setCartId(data.cart_id);
      setProduct(null);
      setCartItems([]);
    } catch (err) {
      setError(err.message);
    }
  };

  const fetchProduct = async (barcode) => {
    setError(null);
    try {
      const res = await fetch(`${API_URL}/product/${barcode}`);
      if (res.status === 404) {
        setProduct(null);
        setError("Product not found");
        return;
      }
      if (!res.ok) throw new Error("Error fetching product");
      const data = await res.json();
      setProduct(data);
    } catch (err) {
      setError(err.message);
      setProduct(null);
    }
  };

  // Add product to cart
  const addToCart = async (barcode) => {
    if (!cartId) {
      setError("Please start a cart session first");
      return;
    }
    setError(null);
    try {
      const res = await fetch(`${API_URL}/cart/${cartId}/add`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ barcode, quantity: 1 }),
      });
      if (!res.ok) throw new Error("Failed to add product to cart");
      await loadCart();
    } catch (err) {
      setError(err.message);
    }
  };

  // Load cart items from backend
  const loadCart = async () => {
    if (!cartId) return;
    setLoadingCart(true);
    setError(null);
    try {
      const res = await fetch(`${API_URL}/cart/${cartId}`);
      if (!res.ok) throw new Error("Failed to load cart");
      const data = await res.json();
      setCartItems(data.items || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingCart(false);
    }
  };

  // On cartId change, load cart items
  useEffect(() => {
    if (cartId) {
      loadCart();
    }
  }, [cartId]);

  const checkout = async () => {
    if (!cartId) {
      setError("No active cart to checkout");
      return;
    }
    setError(null);
    try {
      const res = await fetch(`${API_URL}/cart/${cartId}/checkout`, {
        method: "POST",
      });
      if (!res.ok) throw new Error("Checkout failed");
      const data = await res.json();
      alert(
        `Checkout successful! Order #${data.order_id} Total: ₹${data.total_price}`
      );
      setCartId(null);
      setCartItems([]);
      setProduct(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const onBarcodeScanned = (barcode) => {
    fetchProduct(barcode);
  };
  console.log(cartId)

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6 text-blue-700">
        Virtual Shopping Cart
      </h1>

      {!cartId ? (
        <>
          <button
            onClick={createCartSession}
            className="px-5 py-3 bg-blue-600 text-white rounded shadow hover:bg-blue-700"
          >
            Start Shopping
          </button>
          {error && <p className="mt-4 text-red-600">{error}</p>}
        </>
      ) : (
        <>
          <BarcodeInput onBarcode={onBarcodeScanned} />
          {error && <p className="mt-4 text-red-600">{error}</p>}

          {product && (
            <ProductInfo
              product={product}
              onAdd={() => addToCart(product.barcode)}
            />
          )}

          {loadingCart ? (
            <p>Loading cart...</p>
          ) : (
            <Cart cartItems={cartItems} onLoadCart={loadCart} onCheckout={checkout} />
          )}
        </>
      )}
    </div>
  );
}

export default App;
