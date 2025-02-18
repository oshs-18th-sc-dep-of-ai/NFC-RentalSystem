import "./Home.css";
import Header from "../../components/header";
import Content from "../../components/content";
import Footer from "../../components/footer";
import { Navigate } from "react-router-dom";
import { useState } from "react";

function Home(props) {
  const ID = "Manage"; // 유저아이디

  /*const [isLogined, setIsLogined] = useState(false);

  if (!isLogined) {
    return <Navigate to="/Login" />;
  }*/

  return (
    <div className="Home">
      <Header />
      <Content id={ID} />
      <Footer />
    </div>
  );
}

export default Home;
