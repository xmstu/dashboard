from flask import render_template, redirect

from server import app
from server.meta.login_record import visitor_record
from server.meta.session_operation import SessionOperationClass


@app.route('/introduce/', endpoint='introduce')
@visitor_record
def introduce():
    """省省统计中心介绍页面"""
    if not SessionOperationClass.check():
        return redirect('/login/')
    return render_template('/introduce/introduce.html')
