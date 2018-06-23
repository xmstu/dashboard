from server import app
from flask import render_template, session, redirect

@app.route('/password/')
def password():
    """修改密码"""
    if not session.get('login'):
        return redirect('/login/')
    # 用户名，头像, 地区
    user_name = session['login'].get('user_name', '')
    avatar_url = session['login'].get('avatar_url', 'https://mp.huitouche.com/static/images/newicon.png')
    return render_template('/password/change-password.html', user_name=user_name, avatar_url=avatar_url)