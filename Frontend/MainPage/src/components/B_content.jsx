import React, { useState } from "react";
import "./B_content.css";
import { useLocation } from "react-router-dom";

//gpt에게 압도적 감사를 표합니다...

const Content = () => {
  const location = useLocation();
  const ID = location.state.ID;

  const [selectedItem, setSelectedItem] = useState(null); //선택된 아이템들 담아두는 곳
  const [newItem, setNewItem] = useState({ name: "", count: 0 }); //관리자 아이템 추가한 거
  const [items, setItems] = useState({
    //물품들
    우산: 30,
    보조배터리: 20,
  });
  const [rented, setRented] = useState({
    //대여된 물품 분류용
    우산: { total: 30, rented: [] },
    보조배터리: { total: 20, rented: [] },
  });

  const [toRent, setToRent] = useState([]);
  const [toReturn, setToReturn] = useState([]); // 반납할 물품 추가

  const handleItemSelect = (item) => {
    setSelectedItem(item);
    setToRent([]);
    setToReturn([]); // 물품 선택 시 반납 선택도 초기화
  };

  const handleCheckboxChange = (index) => {
    setToRent((prev) =>
      prev.includes(index) ? prev.filter((i) => i !== index) : [...prev, index]
    );
  };

  const handleReturnCheckboxChange = (index) => {
    setToReturn((prev) =>
      prev.includes(index) ? prev.filter((i) => i !== index) : [...prev, index]
    );
  };

  const handleRent = () => {
    if (window.confirm("정말 대여하시겠습니까?")) {
      // 대여할꺼야아아아앙
      setRented((prev) => ({
        ...prev,
        [selectedItem]: {
          total: prev[selectedItem].total,
          rented: [...prev[selectedItem].rented, ...toRent].sort(
            (a, b) => a - b
          ),
        },
      }));
      setToRent([]);
    }
  };

  const handleReturn = () => {
    if (window.confirm("정말 반납하시겠습니까?")) {
      setRented((prev) => ({
        ...prev,
        [selectedItem]: {
          total: prev[selectedItem].total,
          rented: prev[selectedItem].rented.filter(
            (item) => !toReturn.includes(item)
          ),
        },
      }));
      setToReturn([]);
    }
  };

  const handleAddItem = () => {
    if (newItem.name && !isNaN(newItem.count) && newItem.count > 0) {
      setItems((prev) => ({
        ...prev,
        [newItem.name]: newItem.count,
      }));

      setRented((prev) => ({
        ...prev,
        [newItem.name]: { total: newItem.count, rented: [] },
      }));

      setNewItem({ name: "", count: 0 });
    } else {
      alert("물품 이름과 유효한 개수를 입력해주세요.");
    }
  };

  const handleDeleteItem = (item) => {
    if (window.confirm(`${item}을 정말 삭제하시겠습니까?`)) {
      if (items[item] !== undefined && rented[item] !== undefined) {
        const updatedItems = { ...items }; // 객체 복사
        const updatedRented = { ...rented }; // 객체 복사

        delete updatedItems[item]; // 물품 삭제
        delete updatedRented[item]; // 물품 대여 기록 삭제

        setItems(updatedItems); // 상태 업데이트
        setRented(updatedRented); // 상태 업데이트
      } else {
        alert(`${item}이 존재하지 않습니다.`);
      }
    }
  };

  return (
    <div>
      <div className="container">
        <h1 className="title">물품 대여 시스템</h1>

        {/* 물품 추가 입력 폼 */}
        {ID === "Manage" && (
          <div className="add-item-section">
            <div className="line"></div>
            <h2>물품 추가</h2>
            <div>
              <h4>물품 이름</h4>
              <input
                className="item-add-name"
                type="text"
                placeholder="물품 이름"
                value={newItem.name}
                onChange={(e) =>
                  setNewItem({ ...newItem, name: e.target.value })
                }
              />
            </div>
            <div>
              <h4>물품 개수</h4>
              <input
                className="item-add-count"
                type="number"
                placeholder="물품 개수"
                value={newItem.count}
                onChange={(e) =>
                  setNewItem({ ...newItem, count: parseInt(e.target.value) })
                }
              />
            </div>

            <button className="addButton" onClick={handleAddItem}>
              추가
            </button>
          </div>
        )}

        {/* 물품 삭제 및 선택 UI */}
        {ID === "Manage" && (
          <div className="item-list">
            <h2>물품 목록</h2>
            <div className="itemsAssemble">
              {Object.keys(items).map((item) => (
                <div key={item} className="item-container">
                  <span>
                    {item} ({items[item]})
                  </span>
                  <button onClick={() => handleDeleteItem(item)}>삭제</button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 물품 선택 UI (관리자는 볼 수 없음) */}
        {ID !== "Manage" && (
          <div className="item-selection">
            {Object.keys(items).map((item) => (
              <label key={item} className="radio-label">
                <input
                  type="radio"
                  name="item"
                  value={item}
                  checked={selectedItem === item}
                  onChange={() => handleItemSelect(item)}
                />
                {item} ({items[item]})
              </label>
            ))}
          </div>
        )}

        {/* 대여 시스템 */}
        {ID !== "Manage" && selectedItem && (
          <div className="rental-section">
            <h2 className="subtitle">대여할 {selectedItem} 선택</h2>
            <div className="checkbox-grid">
              {Array.from({ length: items[selectedItem] }).map((_, index) => (
                <div key={index} className="checkbox-container">
                  <input
                    type="checkbox"
                    checked={toRent.includes(index)}
                    onChange={() => handleCheckboxChange(index)}
                    disabled={rented[selectedItem].rented.includes(index)}
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
          </div>
        )}

        {/* 반납 시스템 */}
        {ID !== "Manage" &&
          selectedItem &&
          rented[selectedItem].rented.length > 0 && (
            <div className="return-section">
              <h2 className="subtitle">반납할 {selectedItem} 선택</h2>
              <div className="checkbox-grid">
                {rented[selectedItem].rented.map((index) => (
                  <div key={index} className="checkbox-container">
                    <input
                      type="checkbox"
                      checked={toReturn.includes(index)}
                      onChange={() => handleReturnCheckboxChange(index)}
                    />
                    <div className="checkbox-label">{index + 1}</div>
                  </div>
                ))}
              </div>
              <button
                className="return-button"
                onClick={handleReturn}
                disabled={toReturn.length === 0}
              >
                반납
              </button>
            </div>
          )}

        {/* 대여된 물품 목록 */}
        <div className="rented-list">
          <h3 className="subtitle">대여된 물품</h3>
          {Object.keys(rented).map((item) => (
            <p key={item}>
              {item}:{" "}
              {rented[item].rented
                .sort((a, b) => a - b)
                .map((num) => num + 1)
                .join(", ") || "없음"}
            </p>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Content;
