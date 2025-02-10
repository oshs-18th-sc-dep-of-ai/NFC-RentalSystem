import "./content.css";
import { useLocation } from "react-router-dom";

const Content = () => {
  const location = useLocation();
  return (
    <>
      <div className="Content">
        <h2>
          📆 오늘의 날짜:{location} {new Date().toLocaleDateString()}
        </h2>
        <div className="line"></div>
        <h3>대여현황: 없음</h3> {/*없음에 {}추가하고 대여 현황 상태 해놓기*/}
        <a href="#">
          <div className="Dayeo">🎒양심 물품 대여하기</div>
        </a>
        <div className="text">
          <h4>
            ※빌린 양심 물품은 반납일을 기준으로 <span>2일안에</span> 제출하지
            않을 시 불이익이 있습니다.
            <br />
            <br />
            ※물품 파손시 <span>배상을</span> 해야하므로 소중하게 다뤄주세요.
            <br />
            <br />
            ※그 밖에 문의 사항은 <span>학생회에</span> 문의하십시요.
          </h4>
        </div>
      </div>
    </>
  );
};
export default Content;
