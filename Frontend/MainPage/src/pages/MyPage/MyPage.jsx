import "./MyPage.css";
import React, { useState } from "react";
import Header from "../../components/M_header";
import Content from "../../components/M_content";

function MyPage() {
  return (
    <>
      <div className="Mypage">
        <Header />
        <Content />
      </div>
    </>
  );
}

export default MyPage;
