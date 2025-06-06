import "./B_header.css";
import { Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";

const Header = () => {
  const navigate = useNavigate();
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    const checkSession = async () => {
      try {
        const response = await axios.get("http://localhost:5000/check_session", { withCredentials: true });
        if (response.data.admin_id) {
          setIsAdmin(true);  // ✅ 관리자 세션이 있으면 true 설정
        } else {
          setIsAdmin(false);
        }
      } catch (error) {
        console.error("세션 확인 실패:", error);
        setIsAdmin(false);
      }
    };
    checkSession();
  }, []);

  const handleLogoClick = () => {
    if (isAdmin) {
      navigate("/Borrow");  // ✅ 관리자는 UserManage로 이동
    } else {
      navigate("/");  // ✅ 학생은 홈으로 이동
    }
  };

  return (
    <>
      <div className="Bheader">
        <header className="HeaderObj">
          <img className="photo" alt="학생회로고" src="schooljjang.png"></img>
          <h1 className="logo" onClick={handleLogoClick} style={{ cursor: "pointer" }}>
            양심물품대여
          </h1>
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
