import "./Home.css";
import Header from "../../components/header";
import Content from "../../components/content";
import Footer from "../../components/footer";
import { useLocation } from "react-router-dom";

function Home() {
  const location = useLocation();
  const ID = "Manage";
  const ITEM = { 우산: 30, 보조배터리: 10 };
  return (
    <>
      <div className="Home">
        <Header />
        <Content id={ID} item={ITEM} />
        <Footer />
      </div>
    </>
  );
}

export default Home;
