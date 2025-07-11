import "./M_content.css";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

const Mcontent = () => {
  const [student, setStudent] = useState(null);  // 학생 정보
  const [rentals, setRentals] = useState({});   // 대여 물품 정보

  useEffect(() => {
    // 백엔드에서 학생 프로필 정보 가져오기
    const fetchProfile = async () => {
      try {
        const response = await axios.get("http://localhost:5000/profile", {
          withCredentials: true, // 세션 유지
        });

        if (response.data.status === "success") {
          setStudent(response.data.student);
          setRentals(response.data.rentals);
        } else {
          console.error("프로필 데이터를 불러오는 중 오류 발생:", response.data.message);
        }
      } catch (error) {
        console.error("프로필 API 호출 오류:", error);
      }
    };

    fetchProfile();
  }, []);


  if (!student) {
    return <p>로딩 중...</p>;
  }

  return (
    <div className="Mcontent">
      <div className="Mcontainer">
        <div className="personal">
          <h2>프로필</h2>
          <h3>이름 : {student.student_name}</h3>
          <h3>아이디 : {student.student_id}</h3>
          <Link to={"/Info"} state={{ student }}>
            <img className="icon" alt="변경" src="icon1.png" />
          </Link>
          <div className="line"></div>
          <h2>대여한 물품 및 반납 시간</h2>
          {Object.keys(rentals).length > 0 ? (
            Object.entries(rentals).map(([product, items], index) => (
              <h3 key={index}>
                {product} : {items.map(item => `${item.product_id}번, 반납 시간: ${item.return_time}`).join(" | ")}
              </h3>
            ))
          ) : (
            <h3>대여한 물품이 없습니다.</h3>
          )}
        </div>
      </div>
    </div>
  );
};

export default Mcontent;
