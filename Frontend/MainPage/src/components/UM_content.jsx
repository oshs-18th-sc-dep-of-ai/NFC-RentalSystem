import "./UM_content.css";
import { useRef, useState } from "react";

const Content = (props) => {
  const containerRef = useRef(null); //드래그
  const [isDragging, setIsDragging] = useState(false); //드래그
  const [startX, setStartX] = useState(0); //드래그
  const [scrollLeft, setScrollLeft] = useState(0); //드래그
  let day = new Date().toLocaleDateString().split(". "); //오늘의 날짜

  const handleMouseDown = (e) => {
    //드래그
    if (!containerRef.current) return;
    setIsDragging(true);
    setStartX(e.clientX - containerRef.current.offsetLeft);
    setScrollLeft(containerRef.current.scrollLeft);
  };

  const handleMouseLeaveOrUp = () => {
    //드래그
    setIsDragging(false);
  };

  const handleMouseMove = (e) => {
    //드래그
    if (!isDragging || !containerRef.current) return;
    e.preventDefault();
    const x = e.clientX - containerRef.current.offsetLeft;
    const walk = (x - startX) * 1.5;
    containerRef.current.scrollLeft = scrollLeft - walk;
  };

  function calculateDeadline(m, d) {
    //반납일 계산
    let newD = d + 2;
    let newM = m;
    if (
      (newM <= 7 && newM % 2 === 0 && newD >= 30) ||
      (newM % 2 !== 0 && newD >= 31) ||
      (newM > 7 && newM % 2 === 0 && newD >= 31) ||
      (newM % 2 !== 0 && newD >= 30) ||
      (newM === 2 && newD >= 28)
    ) {
      newM += 1;
      newD -= 30;
    }
    return [2025, newM, newD]; //연도 변수
  }

  const DeleteUser = (id) => {
    setRentalData(rentalData.filter((rental) => rental.id !== id));
  };

  const [rentalData, setRentalData] = useState([
    // 대여한 애들
    {
      id: "20919",
      name: "이가연",
      items: ["우산", "슬리퍼"],
      count: [1, 1],
      date: [2025, 2, 18],
      deadline: calculateDeadline(2, 18),
      state: false,
    },
    {
      id: "20920",
      name: "김철수",
      items: ["우산"],
      count: [2],
      date: [2025, 2, 14],
      deadline: calculateDeadline(2, 16),
      state: false,
    },
    {
      id: "20921",
      name: "박영희",
      items: ["슬리퍼"],
      count: [1],
      date: [2025, 2, 14],
      deadline: calculateDeadline(2, 14),
      state: false,
    },
    {
      id: "20913",
      name: "박지윤",
      items: ["슬리퍼"],
      count: [1],
      date: [2025, 2, 19],
      deadline: calculateDeadline(2, 19),
      state: true,
    },
    {
      id: "20901",
      name: "남블리드",
      items: ["슬리퍼"],
      count: [1],
      date: [2025, 2, 13],
      deadline: calculateDeadline(2, 13),
      state: true,
    },
  ]);

  rentalData.sort((a, b) => {
    const overdueA =
      day[0] > a.deadline[0] ||
      day[1] > a.deadline[1] ||
      day[2] > a.deadline[2];
    const overdueB =
      day[0] > b.deadline[0] ||
      day[1] > b.deadline[1] ||
      day[2] > b.deadline[2];
    const diffA = Math.abs(day[2] - a.deadline[2]);
    const diffB = Math.abs(day[2] - b.deadline[2]);

    // 1. state === true인 항목을 최상단으로 배치
    if (a.state && !b.state) return -1;
    if (!a.state && b.state) return 1;

    // 2. state === true인 항목 중 절댓값 높은 순으로 정렬
    if (a.state && b.state) return diffB - diffA;

    // 3. 기존 연체 여부 및 연체일 기준 정렬
    if (overdueA && !overdueB) return -1;
    if (!overdueA && overdueB) return 1;
    return diffB - diffA;
  });

  return (
    <div className="UMcontent">
      <div className="c">
        <h2>📆 오늘의 날짜: {day.join(". ")}</h2>
        <h2>대여현황</h2>
        <div className="line"></div>
        <div>
          <span className="orange">주황색은</span> 반납 대기중,{" "}
          <span className="purple">보라색은</span> 연체중,{" "}
          <span className="blue">파란색은</span> 정상 상태입니다.
        </div>
        <div
          className="container"
          ref={containerRef}
          onMouseDown={handleMouseDown} //드래그 기능
          onMouseLeave={handleMouseLeaveOrUp}
          onMouseUp={handleMouseLeaveOrUp}
          onMouseMove={handleMouseMove} // 드래그 기능
        >
          {rentalData.map((rental) => {
            const isOverdue =
              day[0] > rental.deadline[0] ||
              day[1] > rental.deadline[1] ||
              day[2] > rental.deadline[2]; //
            const isAllowing = rental.state;
            return (
              <div
                key={rental.id}
                className={`block ${
                  isAllowing ? "highlight" : isOverdue ? "warn" : ""
                }`}
              >
                ID: {rental.id} {rental.name}
                <br />
                대여품:{" "}
                {rental.items
                  .map((item, i) => `${item} ${rental.count[i]}개`)
                  .join(", ")}
                <br />
                대여일: {rental.date.join(".")}
                <br />
                반납일: {rental.deadline.join(".")} (
                {-(day[2] - rental.deadline[2])}){/* 반납 대기중 문구 추가 */}
                <button
                  className={`DeleteButton ${
                    isAllowing ? "highlight" : isOverdue ? "warn" : ""
                  }`}
                  onClick={() => DeleteUser(rental.id)}
                >
                  반납
                </button>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Content;
