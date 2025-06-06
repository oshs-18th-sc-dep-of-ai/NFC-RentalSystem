import React, { useEffect, useState } from "react";
import axios from "axios";
import Header from "../../components/M_header";
import "./MyPage.css";

function MyPage() {
  const [studentInfo, setStudentInfo] = useState(null);
  const [rentals, setRentals] = useState({});

  useEffect(() => {
    axios
      .get("http://localhost:5000/profile", { withCredentials: true })
      .then((response) => {
        setStudentInfo(response.data.student);
        setRentals(response.data.rentals || {});
      })
      .catch((error) => {
        console.error("프로필 정보를 불러오는데 실패했습니다.", error);
      });
  }, []);

  return (
    <div className="Mypage">
      <Header />
      <div className="profile-card">
        <h2>프로필</h2>
        <p>이름: {studentInfo?.student_name}</p>
        <p>아이디: {studentInfo?.student_id}</p>
        <button className="change-password-btn">비밀번호 변경</button>
      </div>

      <div className="profile-card">
        <h2>대여한 물품 및 반납 시간</h2>
        {Object.keys(rentals).length === 0 ? (
          <p>대여한 물품이 없습니다.</p>
        ) : (
          Object.entries(rentals).map(([productName, items]) => (
            <div key={productName} className="rental-item">
              <h3>{productName}</h3>
              <ul>
                {items.map((item, index) => (
                  <li key={index}>
                    제품 ID: {item.product_id}, 반납 예정 시간: {item.return_time}
                  </li>
                ))}
              </ul>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default MyPage;
