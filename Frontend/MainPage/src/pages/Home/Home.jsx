import "./Home.css";
import Header from "../../components/header";
import Content from "../../components/content";
import Footer from "../../components/footer";
import { Navigate } from "react-router-dom";
import { useState } from "react";

function Home(props) {
  const ID = "Manage";
  const ITEM = { 우산: 30, 보조배터리: 10 };

  const [isLogined, setIsLogined] = useState(false);

  if (!isLogined) {
    return <Navigate to="/Login" />;
  }

  return (
    <div className="Home">
      <Header />
      <Content id={ID} item={ITEM} />
      <Footer />
    </div>
  );
}

export default Home;
