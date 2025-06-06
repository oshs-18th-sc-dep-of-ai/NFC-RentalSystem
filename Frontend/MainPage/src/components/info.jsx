import "./info.css";
import { Link } from "react-router-dom";

const Info = () => {
  const ID = "20919 이가연";
  const PW = "20919";
  return (
    <>
      <div className="main">
        <div className="Icontainer">
          <h3>아이디 : {ID}</h3>
          <h3>비밀번호 : {PW}</h3>
          <div className="line"></div>
          <h3>대여한 물품들</h3>
        </div>
      </div>
    </>
  );
};

export default Info;
