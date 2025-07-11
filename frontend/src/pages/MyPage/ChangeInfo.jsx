import React, { useState } from "react";
import axios from "axios";
import Header from "../../components/M_header"; // ✅ 헤더 추가
import "./ChangeInfo.css";

function ChangeInfo() {
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handlePasswordChange = () => {
    if (!newPassword || !confirmPassword) {
      alert("비밀번호를 모두 입력해주세요!");
      return;
    }
    if (newPassword !== confirmPassword) {
      alert("비밀번호가 일치하지 않습니다.");
      return;
    }

    axios.post("http://localhost:5000/change_password", { new_password: newPassword }, { withCredentials: true })
      .then(response => {
        alert(response.data.message);
        setNewPassword("");
        setConfirmPassword("");
      })
      .catch(error => {
        console.error("비밀번호 변경 실패:", error);
        alert("비밀번호 변경 실패");
      });
  };

  return (
    <div className="change-info-page">
      <Header /> {/* ✅ 헤더 렌더링 */}
      <div className="change-info-container">
        <h2>비밀번호 변경</h2>
        <label>새 비밀번호</label>
        <input
          type="password"
          placeholder="새 비밀번호를 입력하세요"
          value={newPassword}
          onChange={e => setNewPassword(e.target.value)}
        />
        <label>새 비밀번호 확인</label>
        <input
          type="password"
          placeholder="다시 한 번 입력하세요"
          value={confirmPassword}
          onChange={e => setConfirmPassword(e.target.value)}
        />
        <button onClick={handlePasswordChange}>비밀번호 변경</button>
      </div>
    </div>
  );
}

export default ChangeInfo;
