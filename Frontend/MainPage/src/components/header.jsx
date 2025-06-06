import "./header.css";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <>
      <div className="Header">
        <header className="HeaderObj">
          <img className="photo" alt="학생회로고" src="schooljjang.png"></img>
          <Link to="/">
            <h1 className="logo">양심물품대여</h1>
          </Link>
          <nav>
            <ul className="nav-links">
              <Link to={"/MyPage"}>
                <img className="photoo" alt="오별이" src="ostar.png"></img>
              </Link>
            </ul>
          </nav>
        </header>
      </div>
    </>
  );
};
export default Header;
