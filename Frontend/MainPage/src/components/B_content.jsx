import React, { useState } from "react";
import "./B_content.css";
import { useLocation } from "react-router-dom";

const Content = () => {
  const location = useLocation();
  const ID = location.state.ID;
  function IsIDManager() {
    if (ID === "Manage") {
      return <div>Hello {ID}</div>;
    } else {
      return <div>{ID}</div>;
    }
  }
  {
    console.log(ID);
  }
  const [selectedItem, setSelectedItem] = useState(null);
  const [items] = useState({
    umbrella: 30, // 우산 개수
    battery: 30, // 보조배터리 개수
  });
  const [rented, setRented] = useState({ umbrella: [], battery: [] });
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
    <div className="container">
      <h1 className="title">물품 대여 시스템</h1>
      <div>{IsIDManager()}</div>
      <div className="item-selection">
        <label className="radio-label">
          <input
            type="radio"
            name="item"
            value="umbrella"
            checked={selectedItem === "umbrella"}
            onChange={() => handleItemSelect("umbrella")}
          />
          우산 ({items.umbrella})
        </label>
        <label className="radio-label">
          <input
            type="radio"
            name="item"
            value="battery"
            checked={selectedItem === "battery"}
            onChange={() => handleItemSelect("battery")}
          />
          보조배터리 ({items.battery})
        </label>
      </div>

      {selectedItem && (
        <div className="rental-section">
          <h2 className="subtitle">
            대여할 {selectedItem === "umbrella" ? "우산" : "보조배터리"} 선택
          </h2>
          <div className="checkbox-grid">
            {Array.from({ length: items[selectedItem] }).map((_, index) => (
              <div key={index} className="checkbox-container">
                <input
                  type="checkbox"
                  checked={toRent.includes(index)}
                  onChange={() => handleCheckboxChange(index)}
                  disabled={rented[selectedItem].includes(index)}
                />
                <div className="checkbox-label">{index + 1}</div>
              </div>
            ))}
          </div>
          <button
            className="rent-button"
            onClick={handleRent}
            disabled={toRent.length === 0}
          >
            대여
          </button>
          <div className="rented-list">
            <h3 className="subtitle">대여된 물품</h3>
            <p>
              우산:{" "}
              {rented.umbrella
                .sort((a, b) => a - b)
                .map((num) => num + 1)
                .join(", ") || "없음"}
            </p>
            <p>
              보조배터리:{" "}
              {rented.battery
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

export default Content;
