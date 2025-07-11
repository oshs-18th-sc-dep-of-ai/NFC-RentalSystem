import React, { useEffect, useState } from "react";
import axios from "axios";
import { useLocation } from "react-router-dom";
import Header from "../../components/B_header";
import "../../components/B_content.css"; // 기존 스타일 재사용

function Return() {
  const location = useLocation();
  const ID = location.state?.ID;
  const [rentals, setRentals] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:5000/profile", { withCredentials: true })
      .then((response) => {
        setRentals(response.data.rentals || []);
      })
      .catch(() => {
        setRentals([]);
      });
  }, []);

  // 반납 요청 함수 (API 엔드포인트에 맞게 수정)
  const handleReturn = async (rental_id) => {
    try {
      await axios.post(
        `http://localhost:5000/rental_request_return/${rental_id}`,
        {},
        { withCredentials: true }
      );
      alert("반납 요청이 완료되었습니다!");
      setRentals((prev) =>
        prev.map((item) =>
          item.rental_id === rental_id ? { ...item, status: "반납 대기 중" } : item
        )
      );
    } catch (error) {
      alert("반납 요청에 실패했습니다.");
    }
  };

  return (
    <div>
      <Header />
      <div className="container">
        <h1 className="title">양심물품반납</h1>
        <h2 className="subtitle">물품 반납 시스템</h2>
        <div style={{ margin: "30px 0" }}>
          <b>대여한 물품 목록</b>
          <div className="rented-list" style={{ marginTop: "10px" }}>
            {rentals.filter((item) => item.status === "대여 중").length === 0 ? (
              <div>반납할 물품이 없습니다.</div>
            ) : (
              rentals
                .filter((item) => item.status === "대여 중")
                .map((item) => (
                  <div key={item.rental_id} style={{ marginBottom: "20px", border: "1px solid #eee", borderRadius: "8px", padding: "10px" }}>
                    <div>
                      <b>{item.product_name}</b> (제품ID: {item.product_id})
                    </div>
                    <div>대여일: {item.rental_time}</div>
                    <button
                      style={{
                        marginTop: "10px",
                        background: "#3493ff",
                        color: "white",
                        border: "none",
                        borderRadius: "5px",
                        padding: "6px 16px",
                        cursor: "pointer",
                      }}
                      onClick={() => handleReturn(item.rental_id)}
                    >
                      반납하기
                    </button>
                  </div>
                ))
            )}
          </div>
        </div>
        <div className="text">
          <h5>
            ※반납 후 <span>2일 이내</span> 미반납 시 불이익이 있습니다.<br />
            ※파손 시 <span>배상</span>해야 하니 소중히 다뤄주세요.<br />
            ※문의는 <span>학생회</span>에 해주세요.
          </h5>
        </div>
      </div>
    </div>
  );
}

export default Return;