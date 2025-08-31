import React, { useState, useEffect } from "react";
import Cart from "@/components/Cart.jsx";
import ProductInfo from "@/components/ProductInfo.jsx";
import BarcodeInput from "@/components/BarcodeInput.jsx";

const API_URL = import.meta.env.REACT_APP_API_URL || "http://localhost:5000";

function App() {
    const [cartId, setCartId] = useState(null);
    const [product, setProduct] = useState(null);
    const [relatedProducts, setRelatedProducts] = useState(null);
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
            setProduct(data["product"]);
            setRelatedProducts(data["related_products"])
        } catch (err) {
            setError(err.message);
            setProduct(null);
        }
    };

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

    const onRemove = async (item) => {
        const barcode = item.barcode;
        try {
            const res = await fetch(`${API_URL}/cart/${cartId}/delete`, {
                method: "DELETE",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ barcode }),
            });
            if (!res.ok) throw new Error("Failed to add product to cart");
            await loadCart();
        } catch (err) {
            setError(err.message);
        }
    }

    const onUpdateQty = async (item, qty) => {
        const barcode = item.barcode
        try {
            const res = await fetch(`${API_URL}/cart/${cartId}/add`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ barcode, quantity: qty }),
            });
            if (!res.ok) throw new Error("Failed to add product to cart");
            await loadCart();
        } catch (err) {
            setError(err.message);
        }
    }

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
                <div className="flex gap-6">
                    <div className="flex-1">
                        <BarcodeInput onBarcode={onBarcodeScanned} />
                        {error && <p className="mt-4 text-red-600">{error}</p>}

                        {product && (
                            <div className="mt-4">
                                <ProductInfo
                                    product={product}
                                    relatedProducts={relatedProducts}
                                    onAdd={() => addToCart(product.barcode)}
                                />
                            </div>
                        )}
                    </div>
                    <Cart cartItems={cartItems} onCheckout={checkout} onRemove={onRemove} onUpdateQty={onUpdateQty} />
                </div>
            )}
        </div>
    );

}

export default App;
