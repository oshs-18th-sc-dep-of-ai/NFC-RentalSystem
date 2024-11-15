import "./header.css";

const Header = () => {
  return (
    <>
      <div className="Header">
        <h3>여러분의 편의를 위해 노력하겠습니다.😊</h3>
        <h1>📆오늘의 날짜: {new Date().toLocaleDateString()}</h1>
      </div>
    </>
  );
};
export default Header;
