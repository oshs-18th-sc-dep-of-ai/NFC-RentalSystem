import React, { useState } from "react";
import "./Login.css";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./styles.css";

function Login() {
  let [id, setId] = useState("");
  let [pw, setPw] = useState("");
  const [showPswd, setShowPswd] = useState(false);
  let navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("ID:", id, "PW:", pw);

    try {
      // ✅ Flask 백엔드 로그인 API 요청
      const response = await axios.post("http://localhost:5000/login", {
        id,   // ✅ 학생과 어드민 모두 "id" 필드로 보냄
        password: pw
      }, { withCredentials: true });

      // ✅ 로그인 성공 시, 백엔드에서 받은 redirect_url로 이동
      if (response.data.status === "success") {
        alert(response.data.message);
        navigate(response.data.redirect_url, { state: { id, student_name: response.data.student_name } });
      }
    } catch (error) {
      alert("로그인 실패: " + (error.response?.data?.message || "서버 오류"));
    }
  };

  return (
    <div className="Login">
      <div className="container">
        <h1>로그인</h1>

        <form onSubmit={handleSubmit}>
          <label className="studentId">아이디:</label>
          <input
            type="text"
            id="studentId"
            name="studentId"
            placeholder="아이디 입력"
            value={id}
            onChange={(e) => setId(e.target.value)}
            required
          />
          <label className="password">비밀번호:</label>
          <input
            type={showPswd ? "text" : "password"}
            id="password"
            name="password"
            placeholder="비밀번호 입력"
            value={pw}
            onChange={(e) => setPw(e.target.value)}
            required
          />
          <label>
            <input type="checkbox" onChange={() => setShowPswd((prev) => !prev)} />
            <span>비밀번호 보기</span>
          </label>
          <button type="submit">로그인</button>
          <p className="info-text">
            기본 비밀번호는 마이페이지에서 변경할 수 있어요!
          </p>
        </form>
      </div>
    </div>
  );
}

export default Login;
