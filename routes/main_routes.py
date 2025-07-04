from flask import Blueprint, render_template, session, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/main')
def main_page():
    # 로그인 확인
    if 'session_student_id' not in session:
        return redirect(url_for('auth.login'))  # 로그인 안 된 경우 로그인 페이지로 리디렉션

    return render_template('mainpage.html')  # 로그인된 경우 메인 페이지 표시
