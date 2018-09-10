from flask import session, render_template
from werkzeug.utils import redirect

from server.cache_data import init_regions
from server.meta.session_operation import sessionOperationClass
from server.status import HTTPStatus


def route_func(route, template_name):
    if not sessionOperationClass.check():
        return redirect('/login/')
    if '超级管理员' not in session['login'].get('role'):
        # 判断路由是否在用户的权限路由中
        if route not in session['login'].get('path'):
            return render_template('/exception/except.html', status_coder=HTTPStatus.Forbidden, title='服务器拒绝该请求',
                                   content='你没有权限访问当前页面')
    # 用户名，头像, 地区
    user_name = session['login'].get('user_name', '')
    account = session['login'].get('account', '')
    avatar_url = session['login'].get('avatar_url', 'https://mp.huitouche.com/static/images/newicon.png')
    locations = [{'region_id': i, 'name': init_regions.to_full_short_name(i)} for i in
                 session['login'].get('locations', [])]
    role = session['login'].get('role', '')
    path = session['login'].get('path', '')
    menu_name = session['login'].get('menu_name', '')
    if '城市经理' in role:
        locations = init_regions.get_city_next_region(session['login'].get('locations', []))
    return render_template(template_name, user_name=user_name, avatar_url=avatar_url, locations=locations,
                           role=role, account=account, path=path, menu_name=menu_name)
