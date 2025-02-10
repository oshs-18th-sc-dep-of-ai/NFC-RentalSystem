import React, { useState } from "react";

const RentalSystem = () => {
  const [selectedItem, setSelectedItem] = useState(null);
  const [items, setItems] = useState({
    umbrella: 10, // 우산 개수
    slipper: 10, // 슬리퍼 개수
  });
  const [rented, setRented] = useState({ umbrella: [], slipper: [] });
  const [toRent, setToRent] = useState([]);

  const handleItemSelect = (item) => {
    setSelectedItem(item);
    setToRent([]);
  };

  const handleCheckboxChange = (index) => {
    setToRent((prev) =>
      prev.includes(index) ? prev.filter((i) => i !== index) : [...prev, index]
    );
  };

  const handleRent = () => {
    if (window.confirm("정말 대여하시겠습니까?")) {
      setRented((prev) => ({
        ...prev,
        [selectedItem]: [...prev[selectedItem], ...toRent].sort(
          (a, b) => a - b
        ),
      }));
      setToRent([]);
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto bg-white rounded-xl shadow-md space-y-4">
      <h1 className="text-xl font-bold text-center">물품 대여 시스템</h1>
      <div className="flex gap-4">
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="radio"
            name="item"
            value="umbrella"
            checked={selectedItem === "umbrella"}
            onChange={() => handleItemSelect("umbrella")}
          />
          우산 ({items.umbrella})
        </label>
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="radio"
            name="item"
            value="slipper"
            checked={selectedItem === "slipper"}
            onChange={() => handleItemSelect("slipper")}
          />
          슬리퍼 ({items.slipper})
        </label>
      </div>

      {selectedItem && (
        <div className="space-y-2">
          <h2 className="text-lg font-semibold">
            대여할 {selectedItem === "umbrella" ? "우산" : "슬리퍼"} 선택
          </h2>
          <div className="grid grid-cols-5 gap-2">
            {Array.from({ length: items[selectedItem] }).map((_, index) => (
              <label key={index} className="flex items-center gap-1">
                <input
                  type="checkbox"
                  checked={toRent.includes(index)}
                  onChange={() => handleCheckboxChange(index)}
                  disabled={rented[selectedItem].includes(index)}
                />
                {index + 1}
              </label>
            ))}
          </div>
          <button
            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-400"
            onClick={handleRent}
            disabled={toRent.length === 0}
          >
            대여
          </button>
          <div className="mt-4 p-2 bg-gray-100 rounded">
            <h3 className="text-lg font-semibold">대여된 물품</h3>
            <p>
              우산:{" "}
              {rented.umbrella
                .sort((a, b) => a - b)
                .map((num) => num + 1)
                .join(", ") || "없음"}
            </p>
            <p>
              슬리퍼:{" "}
              {rented.slipper
                .sort((a, b) => a - b)
                .map((num) => num + 1)
                .join(", ") || "없음"}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default RentalSystem;
