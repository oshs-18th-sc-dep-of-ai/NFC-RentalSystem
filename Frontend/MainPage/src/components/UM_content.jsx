import "./UM_content.css";
import { useRef, useState } from "react";

const Content = (props) => {
  const containerRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);
  const [startX, setStartX] = useState(0);
  const [scrollLeft, setScrollLeft] = useState(0);

  const handleMouseDown = (e) => {
    if (!containerRef.current) return;
    setIsDragging(true);
    setStartX(e.pageX - containerRef.current.offsetLeft);
    setScrollLeft(containerRef.current.scrollLeft);
  };

  const handleMouseLeaveOrUp = () => {
    setIsDragging(false);
  };

  const handleMouseMove = (e) => {
    if (!isDragging || !containerRef.current) return;
    e.preventDefault();
    const x = e.pageX - containerRef.current.offsetLeft;
    const walk = (x - startX) * 2; // 드래그 속도 조정
    containerRef.current.scrollLeft = scrollLeft - walk;
  };

  // 여러 개의 대여 현황 데이터 (예제 데이터)
  const rentalData = [
    {
      id: "20919",
      name: "이가연",
      items: ["우산", "슬리퍼"],
      count: [1, 1],
      date: "2025.02.15",
    },
    {
      id: "20920",
      name: "김철수",
      items: ["우산"],
      count: [2],
      date: "2025.02.14",
    },
    {
      id: "20921",
      name: "박영희",
      items: ["슬리퍼"],
      count: [1],
      date: "2025.02.13",
    },
    {
      id: "20913",
      name: "박지윤",
      items: ["슬리퍼"],
      count: [1],
      date: "2025.02.13",
    },
    {
      id: "20901",
      name: "남블리드",
      items: ["슬리퍼"],
      count: [1],
      date: "2025.02.13",
    },
  ];

  return (
    <div className="UMcontent">
      <div className="c">
        <h2>📆 오늘의 날짜: {new Date().toLocaleDateString()}</h2>
        <h2>대여현황</h2>
        <div className="line"></div>
        <div
          className="container"
          ref={containerRef}
          onMouseDown={handleMouseDown}
          onMouseLeave={handleMouseLeaveOrUp}
          onMouseUp={handleMouseLeaveOrUp}
          onMouseMove={handleMouseMove}
        >
          {rentalData.map((rental, index) => (
            <div
              key={index}
              className={`block ${
                rental.date === "2025.02.15" ? "highlight" : ""
              }`}
            >
              ID: {rental.id} {rental.name}
              <br />
              대여품:{" "}
              {rental.items
                .map((item, i) => `${item} ${rental.count[i]}개`)
                .join(", ")}
              <br />
              대여일: {rental.date}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Content;
