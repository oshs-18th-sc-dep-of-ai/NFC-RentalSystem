// 로그인 버튼 클릭 이벤트
document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault(); // 페이지 새로고침 방지

    // 입력값 가져오기
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // 간단한 로그인 유효성 검사
    if (username === "admin" && password === "1234") {
        alert("로그인 성공!!");
    } else {
        alert("아이디 또는 비밀번호가 잘못되었습니다.");
    }
});
