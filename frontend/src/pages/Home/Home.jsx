import React, { useState, useEffect } from "react";
import { Navigate } from "react-router-dom";
import axios from "axios";
import Header from "../../components/header";
import Content from "../../components/content";
import Footer from "../../components/footer";

axios.defaults.withCredentials = true;

function Home() {
  const [isLogined, setIsLogined] = useState(null); // 로딩 중
  const [user, setUser] = useState(null);

  useEffect(() => {
    const checkSession = async () => {
      try {
        const res = await axios.get("http://localhost:5000/check_session");
        if (res.data.status === "success") {
          setUser(res.data.user); // 서버에서 내려주는 유저 정보
          setIsLogined(true);
        } else {
          setIsLogined(false);
        }
      } catch {
        setIsLogined(false);
      }
    };

    checkSession();
  }, []);

  if (isLogined === null) return <div>Loading...</div>; // 로딩 중 표시
  if (!isLogined) return <Navigate to="/Login" />;

  return (
    <div className="Home">
      <Header />
      <Content id={user?.id} />
      <Footer />
    </div>
  );
}

export default Home;
