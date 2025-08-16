import "./footer.css";

const Footer = () => {
  return (
    <>
      <div>
        <footer className="footer">
          <div className="footer-links">
            <p>학생회 인스타:</p>
            <p>
              {/* 학생회 바뀔 때마다 바꿔주기! */}
              <a href="https://www.instagram.com/os.19.sc/">os_19_sc</a>
            </p>
          </div>
          <p>Made by AI융합부</p>
        </footer>
      </div>
    </>
  );
};
export default Footer;
