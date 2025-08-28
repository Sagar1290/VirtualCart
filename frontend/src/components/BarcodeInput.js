import React, { useRef } from "react";

function BarcodeInput({ onBarcode }) {
  const inputRef = useRef();

  const handleInput = (e) => {
    const value = e.target.value.trim();
    if (value.length >= 8) {
      onBarcode(value);
      inputRef.current.value = "";
    }
  };

  return (
    <input
      ref={inputRef}
      className="border p-2 rounded w-64"
      placeholder="Scan or enter barcode"
      autoFocus
      onChange={handleInput}
    />
  );
}

export default BarcodeInput;
