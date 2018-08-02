# -*- coding: utf-8 -*-

from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.message import MessageSystemModel, MessageUserModel
from server.status import HTTPStatus, make_result, APIStatus
from flask_restful import abort
from server import log
import time


class MessageSystem(object):
    @staticmethod
    @make_decorator
    def get_message_list(params):
        """获取消息列表"""
        count = MessageSystemModel.get_sys_msg_list_count(db.read_bi)
        data = MessageSystemModel.get_sys_msg_list(db.read_bi, params)
        return Response(count=count, data=data)

    @staticmethod
    @make_decorator
    def post_message(params):
        """写入消息"""
        try:
            # 写入系统消息表
            msg_id = MessageSystemModel.insert_system_message(db.write_bi, params)
            # 后台用户
            system_user = MessageSystemModel.get_system_user(db.read_db)
            # 区镇合伙人
            suppliers_user = MessageSystemModel.get_suppliers_user(db.read_db)
            # 网点管理员
            supplier_nodes_user = MessageSystemModel.get_supplier_nodes(db.read_db)
            # 城市经理
            city_manager = MessageSystemModel.get_city_manager(db.read_bi)
            # 推送角色
            if params['push_role'] == 1:
                data = []
                for i in system_user:
                    data.append({
                        'account': i['account'],
                        'role': i['role'],
                        'sys_msg_id': msg_id,
                        'create_time': int(time.time()),
                        'update_time': int(time.time())
                    })
                MessageSystemModel.insert_user_message(db.write_bi, data)
            elif params['push_role'] == 2:
                data = []
                for i in suppliers_user:
                    data.append({
                        'account': i['account'],
                        'role': i['role'],
                        'sys_msg_id': msg_id,
                        'create_time': int(time.time()),
                        'update_time': int(time.time())
                    })
                MessageSystemModel.insert_user_message(db.write_bi, data)
            elif params['push_role'] == 3:
                data = []
                for i in supplier_nodes_user:
                    data.append({
                        'account': i['account'],
                        'role': i['role'],
                        'sys_msg_id': msg_id,
                        'create_time': int(time.time()),
                        'update_time': int(time.time())
                    })
                MessageSystemModel.insert_user_message(db.write_bi, data)
            elif params['push_role'] == 4:
                data = []
                for i in city_manager:
                    data.append({
                        'account': i['account'],
                        'role': i['role'],
                        'sys_msg_id': msg_id,
                        'create_time': int(time.time()),
                        'update_time': int(time.time())
                    })
                MessageSystemModel.insert_user_message(db.write_bi, data)
            else:
                # 去重
                users = city_manager + supplier_nodes_user + suppliers_user + system_user
                repeat = []
                data = []
                for i in users:
                    if i['account'] not in repeat:
                        repeat.append(i['account'])
                        data.append({
                            'account': i['account'],
                            'role': i['role'],
                            'sys_msg_id': msg_id,
                            'create_time': int(time.time()),
                            'update_time': int(time.time())
                        })
                MessageSystemModel.insert_user_message(db.write_bi, data)
            return make_result(APIStatus.Ok), HTTPStatus.Ok

        except Exception as e:
            log.error('消息发布异常: [error: %s]' % e, exc_info=True)
            abort(HTTPStatus.BadRequest, **make_result(HTTPStatus.BadRequest, msg='消息发布异常'))

    @staticmethod
    @make_decorator
    def put_message(params):
        # 查询系统消息
        msg = MessageSystemModel.get_sys_msg_by_id(db.read_bi, params)
        if not msg:
            abort(HTTPStatus.BadRequest, **make_result(HTTPStatus.BadRequest, msg='该消息不存在'))
        if msg['is_deleted'] == 1:
            abort(HTTPStatus.BadRequest, **make_result(HTTPStatus.BadRequest, msg='该消息已被删除'))
        # 删除用户消息
        MessageSystemModel.delete_user_message(db.write_bi, params)
        # 修改系统消息表
        MessageSystemModel.update_system_message(db.write_bi, params)
        # 后台用户
        system_user = MessageSystemModel.get_system_user(db.read_db)
        # 区镇合伙人
        suppliers_user = MessageSystemModel.get_suppliers_user(db.read_db)
        # 网点管理员
        supplier_nodes_user = MessageSystemModel.get_supplier_nodes(db.read_db)
        # 城市经理
        city_manager = MessageSystemModel.get_city_manager(db.read_bi)
        # 推送角色
        if params['push_role'] == 1:
            data = []
            for i in system_user:
                data.append({
                    'account': i['account'],
                    'role': i['role'],
                    'sys_msg_id': params['msg_id'],
                    'create_time': int(time.time()),
                    'update_time': int(time.time())
                })
            MessageSystemModel.insert_user_message(db.write_bi, data)
        elif params['push_role'] == 2:
            data = []
            for i in suppliers_user:
                data.append({
                    'account': i['account'],
                    'role': i['role'],
                    'sys_msg_id': params['msg_id'],
                    'create_time': int(time.time()),
                    'update_time': int(time.time())
                })
            MessageSystemModel.insert_user_message(db.write_bi, data)
        elif params['push_role'] == 3:
            data = []
            for i in supplier_nodes_user:
                data.append({
                    'account': i['account'],
                    'role': i['role'],
                    'sys_msg_id': params['msg_id'],
                    'create_time': int(time.time()),
                    'update_time': int(time.time())
                })
            MessageSystemModel.insert_user_message(db.write_bi, data)
        elif params['push_role'] == 4:
            data = []
            for i in city_manager:
                data.append({
                    'account': i['account'],
                    'role': i['role'],
                    'sys_msg_id': params['msg_id'],
                    'create_time': int(time.time()),
                    'update_time': int(time.time())
                })
            MessageSystemModel.insert_user_message(db.write_bi, data)
        else:
            # 去重
            users = city_manager + supplier_nodes_user + suppliers_user + system_user
            repeat = []
            data = []
            for i in users:
                if i['account'] not in repeat:
                    repeat.append(i['account'])
                    data.append({
                        'account': i['account'],
                        'role': i['role'],
                        'sys_msg_id': params['msg_id'],
                        'create_time': int(time.time()),
                        'update_time': int(time.time())
                    })
            MessageSystemModel.insert_user_message(db.write_bi, data)
        return make_result(APIStatus.Ok), HTTPStatus.Ok

    @staticmethod
    @make_decorator
    def delete_message(params):
        try:
            # 删除用户消息
            MessageSystemModel.delete_user_message(db.write_bi, params)
            # 删除系统消息表
            MessageSystemModel.delete_system_message(db.write_bi, params)
            return make_result(APIStatus.Ok), HTTPStatus.Ok
        except Exception as e:
            log.error('消息删除异常: [error: %s]' % e, exc_info=True)
            abort(HTTPStatus.BadRequest, **make_result(HTTPStatus.BadRequest, msg='消息删除异常'))

class MessageUser(object):
    @staticmethod
    @make_decorator
    def get_message_list(params):
        """获取用户消息列表"""
        # 获取消息总数
        count = MessageUserModel.get_msg_count(db.read_bi, params)
        # 获取未读消息数
        unread = MessageUserModel.get_msg_unread_count(db.read_bi, params)
        # 获取当前分页消息
        data = MessageUserModel.get_msg_data(db.read_bi, params)
        return Response(count=count, unread=unread, data=data)

    @staticmethod
    @make_decorator
    def update_msg_read(params):
        """消息已读"""
        MessageUserModel.update_msg_read(db.write_bi, params)
        return make_result(APIStatus.Ok), HTTPStatus.Ok
