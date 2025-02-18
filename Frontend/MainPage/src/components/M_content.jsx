import "./M_content.css";
import { Link } from "react-router-dom";

const Mcontent = (item) => {
  const ID = "2420919";
  const PW = "20919";
  var items = item;
  return (
    <>
      <div className="Mcontent">
        <div className="Mcontainer">
          <img className="picture" alt="프로필 사진" src="ostar.png"></img>
          <div className="personal">
            <h2>프로필</h2>
            <h3>아이디 : {ID}</h3>
            <h3>비밀번호 : {PW}</h3>
            <Link to={"/Info"}>
              <img className="icon" alt="변경" src="icon1.png"></img>
            </Link>
            <div className="line"></div>
            <h2>대여한 물품들</h2>
            <h3>우산 : {items[0]}</h3>
            <h3>보조배터리 : {item[1]}</h3>
          </div>
        </div>
      </div>
    </>
  );
};

export default Mcontent;
