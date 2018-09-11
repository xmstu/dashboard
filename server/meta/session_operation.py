# -*- coding: utf-8 -*-

import time

from flask import session

from server.logger import log


class SessionOperationClass(object):
    """session操作类"""

    @staticmethod
    def insert(user_info, locations):
        """登录"""
        try:
            session['login'] = {
                'account': user_info['account'],
                'user_id': user_info['id'],
                'user_name': user_info['user_name'] if user_info['user_name'] else '',
                'mobile': user_info['account'],
                'avatar_url': user_info['avatar_url'] if user_info[
                    'avatar_url'] else 'https://mp.huitouche.com/static/images/newicon.png',
                'login_time': time.time(),
                'role': user_info['role'],
                'role_id': user_info['role_id'],
                'locations': locations,
                'role_all_path': user_info['role_all_path'],
                'role_all_menu': user_info['role_all_menu'],
                'role_menu_path': user_info['role_menu_path']
            }

            return True
        except Exception as e:
            log.error('登录信息写入session出错 [ERROR: %s]' % e, exc_info=True)
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
            log.error('session登出出错 [ERROR: %s]' % e, exc_info=True)

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
        region_id = session['login'].get('locations', [])
        return role, region_id

    @staticmethod
    def get_role():
        """获取角色权限"""
        role = session['login']['role']
        user_id = session['login']['user_id']
        return role, user_id

    @staticmethod
    def get_user_locations():
        """获取地区权限"""
        region_id = session['login'].get('locations', [])
        return region_id

    @staticmethod
    def change_role(login, role_info):
        """改变角色"""
        try:
            session['login'] = login
            session['login']['role'] = role_info['role']
            session['login']['role_id'] = role_info['role_id']
            session['login']['locations'] = role_info['locations']
            session['login']['role_all_path'] = role_info['role_all_path']
            session['login']['role_all_menu'] = role_info['role_all_menu']
            session['login']['role_menu_path'] = role_info['role_menu_path']
            return True
        except Exception as e:
            log.error('改变角色出错 [ERROR: %s]' % e, exc_info=True)
            return False

    @staticmethod
    def set_session(key, value):
        try:
            session[key] = value
            return True
        except Exception as e:
            log.error('增加session失败:{}'.format(e))
            return False

    @staticmethod
    def get_session(key):
        try:
            return session[key]
        except Exception as e:
            log.error('获取session失败:{}'.format(e))
