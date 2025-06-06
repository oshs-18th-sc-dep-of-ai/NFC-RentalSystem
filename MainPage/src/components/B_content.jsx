import React, { useState } from "react";
import axios from "axios";
import "./B_content.css";

const Content = ({ ID }) => {
  const [selectedItem, setSelectedItem] = useState(null); // 선택된 아이템
  const [newItem, setNewItem] = useState({ name: "", count: 0 }); // 새 물품 추가
  const [items, setItems] = useState({
    우산: 10,
    보조배터리: 5,
  });
  const [rented, setRented] = useState({
    우산: { total: 10, rented: [] },
    보조배터리: { total: 5, rented: [] },
  });
  const [toRent, setToRent] = useState([]);
  const [toReturn, setToReturn] = useState([]);

  const handleItemSelect = (item) => {
    setSelectedItem(item);
    setToRent([]);
    setToReturn([]);
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

  // ✅ 대여 요청
  const handleRent = async () => {
    if (!selectedItem) {
      alert("먼저 물품을 선택해주세요!");
      return;
    }
    if (toRent.length === 0) {
      alert("대여할 번호를 선택해주세요!");
      return;
    }

    const selectedNumber = toRent[0] + 1; // ✅ 인덱스 -> 번호
    const productName = `${selectedItem} ${selectedNumber}`; // "우산 1" 형태로

    if (window.confirm(`${productName}을 정말 대여하시겠습니까?`)) {
      try {
        const response = await axios.post(
          "http://localhost:5000/rental_request",
          { product_name: productName },
          { withCredentials: true }
        );
        alert(response.data.message);

        // 로컬 상태 업데이트 (선택 해제)
        setRented((prev) => ({
          ...prev,
          [selectedItem]: {
            total: prev[selectedItem].total,
            rented: [...prev[selectedItem].rented, ...toRent].sort((a, b) => a - b),
          },
        }));
        setToRent([]);
      } catch (error) {
        console.error("대여 요청 실패:", error);
        alert(`대여 요청 실패: ${error.response?.data?.message || "서버 오류"}`);
      }
    }
  };

  // ✅ 반납 로직 (프론트 로컬 상태만 갱신)
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

  // ✅ 관리자 - 물품 추가
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

  // ✅ 관리자 - 물품 삭제
  const handleDeleteItem = (item) => {
    if (window.confirm(`${item}을 정말 삭제하시겠습니까?`)) {
      const updatedItems = { ...items };
      const updatedRented = { ...rented };
      delete updatedItems[item];
      delete updatedRented[item];
      setItems(updatedItems);
      setRented(updatedRented);
    }
  };

  return (
    <div>
      <div className="container">
        <h1 className="title">물품 대여 시스템</h1>

        {/* ✅ 관리자 - 물품 추가 */}
        {ID === "caoshsadmin" && (
          <div className="add-item-section">
            <div className="line"></div>
            <h2>물품 추가</h2>
            <div>
              <h4>물품 이름</h4>
              <input
                type="text"
                value={newItem.name}
                onChange={(e) => setNewItem({ ...newItem, name: e.target.value })}
              />
            </div>
            <div>
              <h4>물품 개수</h4>
              <input
                type="number"
                value={newItem.count}
                onChange={(e) =>
                  setNewItem({ ...newItem, count: parseInt(e.target.value) })
                }
              />
            </div>
            <button onClick={handleAddItem}>추가</button>
          </div>
        )}

        {/* ✅ 관리자 - 물품 목록 */}
        {ID === "caoshsadmin" && (
          <div className="item-list">
            <h2>물품 목록</h2>
            <div className="itemsAssemble">
              {Object.keys(items).map((item) => (
                <div key={item} className="item-container">
                  <span>{item} ({items[item]})</span>
                  <button onClick={() => handleDeleteItem(item)}>삭제</button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ✅ 학생 - 물품 선택 */}
        {ID !== "caoshsadmin" && (
          <div className="item-selection">
            {Object.keys(items).map((item) => (
              <label key={item}>
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

        {/* ✅ 학생 - 대여 */}
        {ID !== "caoshsadmin" && selectedItem && (
          <div className="rental-section">
            <h2>{selectedItem} 대여할 번호</h2>
            <div className="checkbox-grid">
              {Array.from({ length: items[selectedItem] }).map((_, index) => (
                <div key={index} className="checkbox-container">
                  <input
                    type="checkbox"
                    checked={toRent.includes(index)}
                    onChange={() => handleCheckboxChange(index)}
                    disabled={rented[selectedItem].rented.includes(index)}
                  />
                  <div>{index + 1}</div>
                </div>
              ))}
            </div>
            <button onClick={handleRent} disabled={toRent.length === 0}>대여</button>
          </div>
        )}

        {/* ✅ 학생 - 반납 */}
        {ID !== "caoshsadmin" && selectedItem && rented[selectedItem].rented.length > 0 && (
          <div className="return-section">
            <h2>{selectedItem} 반납할 번호</h2>
            <div className="checkbox-grid">
              {rented[selectedItem].rented.map((index) => (
                <div key={index} className="checkbox-container">
                  <input
                    type="checkbox"
                    checked={toReturn.includes(index)}
                    onChange={() => handleReturnCheckboxChange(index)}
                  />
                  <div>{index + 1}</div>
                </div>
              ))}
            </div>
            <button onClick={handleReturn} disabled={toReturn.length === 0}>반납</button>
          </div>
        )}

        {/* ✅ 대여 목록 */}
        <div className="rented-list">
          <h3>대여된 물품</h3>
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
