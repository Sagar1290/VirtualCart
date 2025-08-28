import React from 'react';

function ProductInfo({ product, onAdd }) {
  return (
    <div className="border p-5 rounded-lg shadow w-72 bg-white">
      <h4 className="text-lg font-bold text-gray-800">{product.name}</h4>
      <p className="text-sm text-gray-600 mb-1">Brand: {product.brand}</p>
      <p className="text-sm text-blue-600 font-semibold">Price: ₹{product.price}</p>
      <button 
        className="mt-2 px-3 py-1 bg-green-500 text-white font-semibold rounded hover:bg-green-600"
        onClick={onAdd}
      >Add to Cart</button>
    </div>
  );
}
export default ProductInfo;
