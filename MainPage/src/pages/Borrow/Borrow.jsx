import "./Borrow.css";
import React, { useState } from "react";
import Header from "../../components/B_header";
import Content from "../../components/B_content";
import { useLocation } from "react-router-dom";
import axios from "axios";
axios.defaults.withCredentials = true;

function Borrow() {
  const location = useLocation();
  const id = location.state?.ID || "UNKNOWN";  // ✅ undefined 방지
  console.log("📢 Borrow.jsx - ID:", id);  // ✅ 디버깅 로그 추가!

  return (
    <>
      <div className="Borrow">
        <Header />
        <Content ID={id} />  // ✅ props로 넘김
      </div>
    </>
  );
}

export default Borrow;
