// Login.js
import React from 'react';
import './styles.css'; // 기존 CSS 파일을 가져옵니다.

function Login() {
  return (
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

        <label htmlFor="password">비밀번호:</label>
        <input
          type="password"
          id="password"
          name="password"
          placeholder="비밀번호를 입력해 주세요"
          required
        />

        <button type="submit">로그인</button>
      </form>
      <p info="info-text">기본 비밀번호는 마이페이지에서 변경할 수 있어요!</p>
      <div className="logo-container">
    <img src="/images/os.png" alt="오성고 로고" />
    <img src="/images/os_18_sc.png" alt="천안오성고 로고" />
</div>

    </div>
  );
}

export default Login;