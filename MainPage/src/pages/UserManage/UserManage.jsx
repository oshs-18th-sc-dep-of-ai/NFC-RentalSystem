import "./UserManage.css";
import React, { useEffect, useState } from "react";
import Header from "../../components/UM_header";
import Content from "../../components/UM_content";
import axios from "axios";
axios.defaults.withCredentials = true;  // ✅ 모든 요청에 credentials 포함

function UserManage() {
  const [adminID, setAdminID] = useState(null);

  useEffect(() => {
    // ✅ 세션 확인 API 요청
    axios.get("http://localhost:5000/check-session")
      .then((res) => {
        console.log("📢 세션 정보:", res.data); // 디버깅용
        setAdminID(res.data.admin_id);  // ✅ 세션에서 admin_id 가져옴
      })
      .catch((err) => {
        console.error("세션 확인 실패:", err);
      });
  }, []);

  return (
    <>
      <div className="UserManage">
        <Header />
        {adminID ? <Content ID={adminID} /> : <p>세션 확인 중...</p>}
      </div>
    </>
  );
}

export default UserManage;
