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
    {
      id: "20919",
      name: "이가연",
      items: ["우산", "슬리퍼"],
      count: [1, 1],
      date: [2025, 2, 18],
      deadline: calculateDeadline(2, 18),
    },
    {
      id: "20920",
      name: "김철수",
      items: ["우산"],
      count: [2],
      date: [2025, 2, 14],
      deadline: calculateDeadline(2, 14),
    },
    {
      id: "20921",
      name: "박영희",
      items: ["슬리퍼"],
      count: [1],
      date: [2025, 2, 14],
      deadline: calculateDeadline(2, 14),
    },
    {
      id: "20913",
      name: "박지윤",
      items: ["슬리퍼"],
      count: [1],
      date: [2025, 2, 16],
      deadline: calculateDeadline(2, 16),
    },
    {
      id: "20901",
      name: "남블리드",
      items: ["슬리퍼"],
      count: [1],
      date: [2025, 2, 13],
      deadline: calculateDeadline(2, 13),
    },
  ]);

  rentalData.sort((a, b) => {
    //연체된 애들 위로 올리기
    const overdueA = day[1] > a.deadline[1] || day[2] > a.deadline[2];
    const overdueB = day[1] > b.deadline[1] || day[2] > b.deadline[2];
    const diffA = Math.abs(day[2] - a.deadline[2]); //별건 아니고 그 연체일 절댓값...
    const diffB = Math.abs(day[2] - b.deadline[2]);

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
              day[1] > rental.deadline[1] || day[2] > rental.deadline[2]; //연체된 애들 중 오래된 순으로 정렬
            return (
              <div
                key={rental.id}
                className={`block ${isOverdue ? "highlight" : ""}`}
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
                {-(day[2] - rental.deadline[2])})
                <button
                  className={`DeleteButton ${isOverdue ? "highlight" : ""}`}
                  onClick={() => DeleteUser(rental.id)}
                >
                  반납
                </button>
                {/*강제 반납처리*/}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Content;
