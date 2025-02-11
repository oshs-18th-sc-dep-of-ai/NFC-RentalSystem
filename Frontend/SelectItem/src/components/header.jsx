import "./header.css";

const Header = () => {
  return (
    <>
      <div className="Header">
        <header className="HeaderObj">
          <img className="photo" alt="학생회로고" src="schooljjang.png"></img>
          <a href="#">
            <h1 className="logo">양심물품대여</h1>
          </a>
          <nav>
            <ul className="nav-links">
              <a href="#">
                <img className="photoo" alt="오별이" src="ostar.png"></img>
              </a>
            </ul>
          </nav>
        </header>
      </div>
    </>
  );
};
export default Header;
