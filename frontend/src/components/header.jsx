import "./header.css";
import { Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
axios.defaults.withCredentials = true; // ✅ 세션 유지

const Header = () => {
  const navigate = useNavigate();
  const [role, setRole] = useState(null); // ✅ 역할 저장 (학생 or 관리자)

  useEffect(() => {
    // ✅ 세션 확인 요청
    axios
      .get("http://localhost:5000/check_session")
      .then((response) => {
        if (response.data.admin_id) {
          setRole("admin"); // ✅ 관리자 로그인 상태
        } else {
          setRole("student"); // ✅ 학생 로그인 상태
        }
      })
      .catch(() => {
        setRole("student"); // 기본값: 학생 (에러 시)
      });
  }, []);

  return (
    <>
      <div className="Header">
        <header className="HeaderObj">
          <img className="photo" alt="학생회로고" src="schooljjang.png"></img>
          {/* ✅ 관리자면 /UserManage로 이동, 학생이면 / 로 이동 */}
          <h1
            className="logo"
            onClick={() => navigate(role === "admin" ? "/UserManage" : "/")}
            style={{ cursor: "pointer" }} // 클릭 가능하게 설정
          >
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
