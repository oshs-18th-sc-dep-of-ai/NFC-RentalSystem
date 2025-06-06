import "./UserManage.css";
import React, { useState } from "react";
import Header from "../../components/UM_header";
import Content from "../../components/UM_content";
import { useLocation } from "react-router-dom";

function UserManage() {
  const location = useLocation();
  const id = location.state.ID;
  return (
    <>
      <div className="UserManage">
        <Header />
        <Content Id={id} />
      </div>
    </>
  );
}

export default UserManage;
