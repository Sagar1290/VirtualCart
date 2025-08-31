



const ProductInfo = ({ product, relatedProducts = [], onAdd }) => {
    const discountedPrice =
        product.discount > 0
            ? (product.price - (product.price * product.discount) / 100).toFixed(2)
            : product.price;

    return (
        <div className="flex justify-center items-top gap-4 flex-row h-full">

            <div className="relative border p-4 rounded-xl shadow-md w-80 bg-white hover:shadow-lg transition">
                {product.discount > 0 && (
                    <span className="absolute top-2 right-2 bg-yellow-400 text-xs font-bold px-2 py-1 rounded">
                        {product.discount}% OFF
                    </span>
                )}
                <img
                    src={product.image_url}
                    alt={product.name}
                    className="w-full h-40 object-contain mb-3"
                />
                <h4 className="text-lg font-bold text-gray-800">{product.name}</h4>
                <p className="text-sm text-gray-500">Brand: {product.brand}</p>

                {product.discount > 0 ? (
                    <p className="text-sm">
                        <span className="line-through text-gray-400 mr-2">₹{product.price}</span>
                        <span className="text-green-600 font-semibold">₹{discountedPrice}</span>
                    </p>
                ) : (
                    <p className="text-blue-600 font-semibold">₹{product.price}</p>
                )}

                <button
                    className="mt-3 w-full py-2 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition"
                    onClick={onAdd}
                >
                    Add to Cart
                </button>
            </div>

            {relatedProducts.length > 0 && (
                <div className="relative border p-4 rounded-xl shadow-md  bg-white hover:shadow-lg transition w-full">
                    <h3 className="text-md font-semibold text-gray-700 mb-2">
                        More from {product.class}
                    </h3>
                    <div className="grid grid-cols-2 gap-3">
                        {relatedProducts.map((item) => {
                            const itemDiscountedPrice =
                                item.discount > 0
                                    ? (item.price - (item.price * item.discount) / 100).toFixed(2)
                                    : item.price;

                            return (
                                <div
                                    key={item.barcode}
                                    className="border p-2 rounded-lg shadow-sm bg-white hover:shadow-md transition"
                                >
                                    {item.discount > 0 && (
                                        <span className="absolute top-1 right-1 bg-yellow-300 text-[10px] font-bold px-1 py-[2px] rounded">
                                            {item.discount}% OFF
                                        </span>
                                    )}
                                    <img
                                        src={item.image_url}
                                        alt={item.name}
                                        className="w-full h-20 object-contain mb-1"
                                    />
                                    <p className="text-xs font-semibold">{item.name}</p>
                                    <p className="text-[11px] text-gray-500">{item.brand}</p>
                                    <p className="text-xs text-green-600 font-bold">
                                        ₹{itemDiscountedPrice}
                                    </p>
                                </div>
                            );
                        })}
                    </div>
                </div>
            )}
        </div>
    );
}

export default ProductInfo;
