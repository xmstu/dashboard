# -*- coding: utf-8 -*-

import time

from flask import request, session

from server.database import db
from server.models.visitor_record import VisitorRecordModel


# 访客记录信息
def visitor_record(f):
    def insert_db(*args, **kwargs):
        if session.get('login'):
            visit_data = {
                'url': request.url if request.url else '',
                'ip': request.headers.get('X-Real-IP', request.remote_addr),
                'user_agent': request.headers.get('User-Agent', ''),
                'user_id': session['login'].get('user_id', 0),
                'user_name': session['login'].get('user_name', ''),
                'user_role': session['login'].get('role_id', 0),
                'visit_time': int(time.time())
            }
            VisitorRecordModel.add_record(db.write_bi, visit_data)
        return f(*args, **kwargs)

    return insert_db
