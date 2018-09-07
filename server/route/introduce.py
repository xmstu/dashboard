from server import app
from flask import render_template, session, redirect
from server.cache_data import init_regions
from server.meta.session_operation import sessionOperationClass
from server.meta.login_record import visitor_record


@app.route('/introduce/', endpoint='introduce')
@visitor_record
def introduce():
    """货源统计页面"""
    if not sessionOperationClass.check():
        return redirect('/login/')
    # 用户名，头像, 地区
    user_name = session['login'].get('user_name', '')
    account = session['login'].get('account', '')
    avatar_url = session['login'].get('avatar_url', 'https://mp.huitouche.com/static/images/newicon.png')
    locations = [{'region_id': i, 'name': init_regions.to_full_short_name(i)} for i in session['login'].get('locations', [])]
    role = session['login'].get('role', 0)
    if role == 4:
        locations = init_regions.get_city_next_region(session['login'].get('locations', []))
    return render_template('/introduce/introduce.html', user_name=user_name, avatar_url=avatar_url, locations=locations, role=role, account=account)