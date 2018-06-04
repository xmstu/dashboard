# -*- coding: utf-8 -*-

from server import app
from server.database import mongo
from server.models import RegionsModel
from server.database import db
from flask import render_template, session, redirect

@app.route('/user/')
def user():
    """用户统计页面"""
    if not session.get('login'):
        return redirect('/login/')
    # 用户名，头像
    user_name = session['login'].get('user_name')
    avatar_url = session['login'].get('avatar_url')
    role = session['login'].get('role')
    # 地区
    locations = []
    # 全部
    if role == 1:
        result = mongo.user_locations.collection.aggregate([{
            '$group': {'_id': {'province_id': '$province_id', 'city_id': '$city_id', 'county_id': '$county_id'}}
        }])
        for location in result:
            region_name = {}
            # 存在市、区
            if location['_id']['county_id']:
                region_name = RegionsModel.get_region_by_code(db.read_db, location['_id']['county_id'])
            elif location['_id']['city_id']:
                region_name = RegionsModel.get_region_by_code(db.read_db, location['_id']['city_id'])
            if region_name and region_name['full_short_name']:
                locations.append({
                    'region_id': region_name['code'],
                    'name': region_name['full_short_name']
                })
    # 部分
    elif role == 2:
        result = RegionsModel.get_user_region(db.read_db, session['user_id'])
        for location in result:
            if location['region_id'] and location['full_short_name']:
                locations.append({
                    'region_id': location['region_id'],
                    'name': location['full_short_name']
                })
    return render_template('/user/user-statistics.html', user_name=user_name, avatar_url=avatar_url, locations=locations)