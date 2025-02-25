import React from "react";
import "./Login.css"; // CSS 가져오기
import { useState } from "react";
import { Navigate } from "react-router-dom";

import { useNavigate } from "react-router-dom"; // useNavigate 추가

function Login() {
  let [id, setId] = useState("");
  let [pw, setPw] = useState("");
  const [showPswd, setShowPswd] = useState(false);
  let navigate = useNavigate(); // 네비게이션 훅 사용

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("ID:", id, "PW:", pw);

    // 로그인 성공 후 홈으로 이동
    navigate("/", { state: { id, pw } });
  };

  const ShowPwCheck = () => {
    setShowPswd((prev) => !prev); // 이전 값의 반대로 변경
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
            placeholder="7자리 숫자"
            value={id}
            onChange={(e) => setId(e.target.value)}
            required
          />
          <label className="password">비밀번호:</label>
          <input
            type={showPswd ? "text" : "password"}
            id="password"
            name="password"
            placeholder="비밀번호를 입력해 주세요"
            value={pw}
            onChange={(e) => setPw(e.target.value)}
            required
          />
          <label>
            <input type="checkbox" onChange={ShowPwCheck} />
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
