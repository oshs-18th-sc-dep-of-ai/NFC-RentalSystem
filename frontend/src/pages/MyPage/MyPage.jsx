import React, { useEffect, useState } from "react";
import axios from "axios";
import Header from "../../components/M_header";
import "./MyPage.css";
import { useNavigate } from "react-router-dom";

function MyPage() {
  const [studentInfo, setStudentInfo] = useState(null);
  const [rentals, setRentals] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios
      .get("http://localhost:5000/profile", { withCredentials: true })
      .then((response) => {
        setStudentInfo(response.data.student);
        setRentals(response.data.rentals || []);
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
        <button
          className="change-password-btn"
          onClick={() => navigate("/info")}
        >
          비밀번호 변경
        </button>
      </div>

      <div className="profile-card">
        <h2>대여/반납 내역</h2>
        {rentals.length === 0 ? (
          <p>대여한 물품이 없습니다.</p>
        ) : (
          <table className="rental-table">
            <thead>
              <tr>
                <th>물품명</th>
                <th>대여일</th>
                <th>반납일</th>
                <th>상태</th>
                <th>반납 예정까지</th>
              </tr>
            </thead>
            <tbody>
              {rentals.map((item, idx) => {
                // 남은 시간 계산
                let leftText = "-";
                if (item.expected_return_time) {
                  const now = new Date();
                  const expected = new Date(item.expected_return_time);
                  let diff = expected - now;
                  if (diff > 0) {
                    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
                    diff -= days * (1000 * 60 * 60 * 24);
                    const hours = Math.floor(diff / (1000 * 60 * 60));
                    diff -= hours * (1000 * 60 * 60);
                    const minutes = Math.floor(diff / (1000 * 60));
                    leftText = `${days}일 ${hours}시간 ${minutes}분 남음`;
                  } else if (Math.abs(diff) < 1000 * 60) {
                    leftText = "지금까지";
                  } else {
                    leftText = "연체";
                  }
                }

                return (
                  <tr key={idx}>
                    <td>{item.product_name}</td>
                    <td>{item.rental_time}</td>
                    <td>{item.return_time || "미정"}</td>
                    <td>{item.status}</td>
                    <td>{leftText}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default MyPage;
