import "./Borrow.css";
import React, { useState } from "react";
import Header from "../../components/B_header";
import Content from "../../components/B_content";
import { useLocation } from "react-router-dom";

function Borrow() {
  const location = useLocation();
  const id = location.state.ID;
  return (
    <>
      <div className="Borrow">
        <Header />
        <Content Id={id} />
      </div>
    </>
  );
}

export default Borrow;
