# -*- coding: utf-8 -*-

from flask import session
from server.logger import log
import time

class sessionOperationClass(object):
    """session操作类"""
    @staticmethod
    def insert(user_info, role, locations):
        """登录"""
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

            return True
        except Exception as e:
            log.error('登录信息写入session出错 [ERROR: %s]' % e)
            return False

    @staticmethod
    def deleted():
        """登出"""
        try:
            if not session.get('login'):
                return False
            session.pop('login')
            return True
        except Exception as e:
            log.error('session登出出错 [ERROR: %s]' % e)

    @staticmethod
    def check():
        """检查是否登录"""
        if session.get('login'):
            return True
        return False

    @staticmethod
    def get_locations():
        """获取角色和地区权限"""
        role = session['login']['role']
        region_id = [str(i) for i in session['login'].get('locations', [])]
        return role, region_id