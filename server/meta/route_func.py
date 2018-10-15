import time

from flask import session, render_template, redirect

from server.cache_data import init_regions
from server.database import db
from server.models.login import Login


def common_route_func(template_name):
    # 用户名，头像, 地区
    user_name = session['login'].get('user_name', '')
    avatar_url = session['login'].get('avatar_url', 'https://mp.huitouche.com/static/images/newicon.png')
    locations = [{'region_id': i, 'name': init_regions.to_full_short_name(i)} for i in
                 session['login'].get('locations', [])]
    role = session['login'].get('role', '')
    role_type = session['login'].get('role_type', '')
    _, role_menu_path = Login.get_menu_path_by_role_id(db.read_bi, session['login'].get('role_id', 0))

    random_num = "?_=" + str(int(time.time()))
    version = 1.1

    if role_type == 4:
        locations = init_regions.get_city_next_region(session['login'].get('locations', []))
    return render_template(template_name, user_name=user_name, avatar_url=avatar_url, locations=locations,
                           role=role, role_type=role_type, role_menu_path=role_menu_path, random_num=random_num, version=version)


def open_route_func(template_name):
    if not session.get('login'):
        return redirect('/login/')

    return common_route_func(template_name)


def close_route_func(route, template_name):
    if not session.get('login'):
        return redirect('/login/')

    if session['login'].get('role') != "超级管理员":
        role_all_path, _ = Login.get_menu_path_by_role_id(db.read_bi, session['login'].get('role_id', 0))
        # 判断路由是否在用户的权限路由中
        if route not in role_all_path:
            return redirect('/home/')
    return common_route_func(template_name)
