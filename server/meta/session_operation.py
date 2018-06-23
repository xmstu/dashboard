# -*- coding: utf-8 -*-

from flask import session
from server.logger import log
import time

class sessionOperationClass(object):
    """session操作类"""
    @staticmethod
    def insert(user_info, role, locations):
        try:
            session['login'] = {
                'user_id': user_info['id'],
                'user_name': user_info['user_name'] if user_info['user_name'] else '',
                'mobile': user_info['mobile'],
                'avatar_url': user_info['avatar_url'] if user_info[
                    'avatar_url'] else 'https://mp.huitouche.com/static/images/newicon.png',
                'login_time': time.time(),
                'role': role,
                'locations': locations
            }
            data = {
                'user_name': user_info['user_name'] if user_info['user_name'] else '',
                'avatar_url': user_info['avatar_url'] if user_info[
                    'avatar_url'] else 'https://mp.huitouche.com/static/images/newicon.png'
            }
            return
        except Exception as e:
            log.error('登录信息写入session出错 [ERROR: %s]' % e)