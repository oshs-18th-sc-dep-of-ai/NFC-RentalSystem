import "./Home.css";
import Header from "../../components/header";
import Content from "../../components/content";
import Footer from "../../components/footer";
import { useState } from "react";
import { useLocation, Navigate } from "react-router-dom";
import axios from "axios";
axios.defaults.withCredentials = true; // ✅ 모든 요청에 credentials 포함

function Home(props) {
  const location = useLocation();
  const user = location.state; // 로그인 시 전달된 id, pw 정보
  const [isLogined, setIsLogined] = useState(user ? true : false);

  if (!isLogined) {
    return <Navigate to="/Login" />;
  }

  return (
    <div className="Home">
      <Header />
      <Content id={user?.id} />
      <Footer />
    </div>
  );
}

export default Home;
