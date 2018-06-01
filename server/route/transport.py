from server import app
from flask import render_template, session, redirect
@app.route('/transport/')
def transport():
    """货源统计页面"""
    if not session.get('login'):
        return redirect('/login/')
    return render_template('/transport/transport-capacity.html')