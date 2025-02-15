import React from "react";
import "./Login.css"; // CSS 가져오기

function Login() {
  return (
    <>
      <div className="Login">
        <div className="container">
          <h1>로그인</h1>
          <form>
            <label htmlFor="studentId">학번:</label>
            <input
              type="text"
              id="studentId"
              name="studentId"
              placeholder="7자리 숫자"
              required
            />

            <label htmlFor="name">이름:</label>
            <input
              type="text"
              id="name"
              name="name"
              placeholder="이름을 입력해 주세요"
              required
            />

            <button type="submit">로그인</button>
          </form>
        </div>
      </div>
    </>
  );
}

export default Login;
