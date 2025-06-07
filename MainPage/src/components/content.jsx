import "./content.css";
import { Link, useLocation } from "react-router-dom";

const Content = () => {
  const location = useLocation();
  const ID = location.state?.id; 

  function IsIDManager() {
    if (ID === "caoshsadmin") {
      return (
        <>
          <Link to={"/Borrow"} state={{ ID }}>
            <div className="Dayeo">🎒양심 물품 관리하기</div>
          </Link>
          <br />
          <Link to={"/UserManage"} state={{ ID }}>
            <div className="Dayeo">🎒사용자 관리하기</div>
          </Link>
          <div className="text">
            <h5>
              ※관리자들께선 <span>2일안에</span> 제출하지 않은 학생들을 잘
              관리해주세요.
              <br />
              <br />※<span>양심 물품 관리하기는</span> 양심 물품을 추가 및
              삭제를 하실 수 있습니다. <span>사용자 관리하기는</span> 학생들의
              대여 상황을 관리할 수 있습니다.
              <br />
              <br />
              ※그 밖에 오류 관련 문의 사항은 <span>AI융합부에게</span>{" "}
              문의하십시오.
            </h5>
          </div>
        </>
      );
    } else if (ID) {
      return (
        <>
          <Link to={"/Borrow"} state={{ ID }}>
            <div className="Dayeo">🎒양심 물품 대여하기</div>
          </Link>
          <Link to={"/Return"} state={{ ID }}>
            <div className="Dayeo" style={{ marginTop: "10px", background: "3493ff" }}>
              📥양심 물품 반납하기
            </div>
          </Link>
          <div className="text">
            <h5>
              ※빌린 양심 물품은 반납일을 기준으로 <span>2일안에</span> 제출하지
              않을 시 불이익이 있습니다.
              <br />
              <br />
              ※물품 파손시 <span>배상을</span> 해야하므로 소중하게 다뤄주세요.
              <br />
              <br />
              ※그 밖에 문의 사항은 <span>학생회에</span> 문의하십시오.
            </h5>
          </div>
        </>
      );
    } else {
      // ID가 없을 때
      return <div>잘못된 접근입니다. 다시 로그인 해주세요.</div>;
    }
  }

  return (
    <div className="Content">
      <div className="c">
        <h2>📆 오늘의 날짜: {new Date().toLocaleDateString()}</h2>
        <h3>여러분의 편의를 위해 노력하겠습니다.😊</h3>
        <div className="line"></div>
        {IsIDManager()}
      </div>
    </div>
  );
};

export default Content;
