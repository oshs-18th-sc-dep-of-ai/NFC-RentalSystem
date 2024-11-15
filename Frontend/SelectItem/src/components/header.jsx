import "./header.css";

const Header = () => {
  return (
    <>
      <div className="Header">
        <h1>오늘의 날짜: {new Date().toLocaleDateString()}😊</h1>
      </div>
    </>
  );
};
export default Header;
