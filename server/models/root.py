import time

from flask_restful import abort

from server import log
from server.status import HTTPStatus, make_result, APIStatus


class RootManagementModel(object):

    @staticmethod
    def get_data(cursor, params):

        fields = """
        tb_inf_admins.id,
        account,
        user_name,
        GROUP_CONCAT(`name`) role_name,
        tb_inf_admins.is_deleted
        """

        command = """
        SELECT
            {fields}
        FROM
            `tb_inf_admins`
            INNER JOIN tb_inf_admin_roles ON tb_inf_admin_roles.admin_id = tb_inf_admins.id AND tb_inf_admin_roles.is_deleted = 0
            INNER JOIN tb_inf_roles ON tb_inf_roles.id = tb_inf_admin_roles.role_id AND tb_inf_roles.is_deleted = 0
        GROUP BY
            tb_inf_admins.id
        """

        count = cursor.query_one(command.format(fields="""COUNT(1) count"""))['count']

        command += """ LIMIT {0}, {1} """.format(params.get('page'), params.get('limit'))

        city_manager_list = cursor.query(command.format(fields=fields))

        data = {
            'city_manager_list': city_manager_list if city_manager_list else [],
            'count': count if count else 0
        }

        return data

    @staticmethod
    def get_role(cursor, admin_id):
        try:
            cmd = """
            SELECT
                role_id,
                `name`
            FROM
                tb_inf_admin_roles
                INNER JOIN tb_inf_roles ON tb_inf_roles.id = tb_inf_admin_roles.role_id
            WHERE
                admin_id = %d
            """ % admin_id
            role_list = cursor.query(cmd)

            role_list = [{i['role_id']: i['name']} for i in role_list]

            return role_list
        except Exception as e:
            log.error('获取用角色失败,失败原因是:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_result(status=APIStatus.BadRequest, msg='请求参数有误'))

    @staticmethod
    def put_data(cursor, params):
        try:
            admin_id = params.pop('admin_id', 0)
            role_id = params.pop('role_id', 0)
            is_active = params.pop('is_active', 0)
            with cursor.begin() as tran:
                update_sql = """id=id"""
                if admin_id:
                    update_list = (', {0}={1}'.format(key, "'" + value + "'" if isinstance(value, str) else value) for
                                   key, value in params.items() if value)
                    for i in update_list:
                        update_sql += i

                    # 是否激活该用户
                    if is_active:
                        if is_active == 1:
                            is_deleted = 0
                        elif is_active == 2:
                            is_deleted = 1
                        update_sql += """, is_deleted={}""".format(is_deleted)

                    command = """
                            UPDATE tb_inf_admins
                            SET {update_sql}
                            WHERE id=:admin_id
                            """

                    rowcount = tran.conn.update(command.format(update_sql=update_sql), args={"admin_id": admin_id})

                    if role_id:
                        # 查出所有当前用户的角色id
                        role_id_list = tran.conn.query("""SELECT role_id FROM tb_inf_admin_roles WHERE admin_id = %d""" % admin_id)
                        role_id_list = [i['role_id'] for i in role_id_list]
                        if role_id not in role_id_list:
                            admin_role_id = tran.conn.insert("""INSERT INTO tb_inf_admin_roles(admin_id, role_id) VALUES(%d, %d)""" % (admin_id, role_id))
                            if admin_role_id:
                                return True
                    else:
                        return rowcount
        except Exception as e:
            log.error('更新用户失败,失败原因是:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_result(status=APIStatus.InternalServerError, msg='服务器内部错误,更新管理后台用户失败'))



    @staticmethod
    def delete_data(cursor, params):
        try:
            with cursor.begin() as tran:
                command = """
                        UPDATE tb_inf_admins
                        SET is_deleted = 1
                        WHERE id=:admin_id
                        """

                rowcount = tran.conn.update(command, params)
                return rowcount
        except Exception as e:
            log.error('删除用户失败,失败原因是:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_result(status=APIStatus.InternalServerError, msg='服务器内部错误,删除管理后台用户失败'))

    @staticmethod
    def post_data(cursor, params):
        try:
            with cursor.begin() as tran:
                admin_command = """
                        INSERT INTO tb_inf_admins(account, password, user_name, avatar_url) 
                        VALUES(:account, :password, :user_name, :avatar_url)
                        """

                params['avatar_url'] = 'https://mp.huitouche.com/static/images/newicon.png'

                admin_id = tran.conn.insert(admin_command, params)

                role_command = """
                        INSERT INTO tb_inf_admin_roles(admin_id, role_id, create_time, update_time) 
                        VALUES(:admin_id, :role_id, :create_time, :update_time)
                """

                params['admin_id'] = admin_id
                params['create_time'] = int(time.time())
                params['update_time'] = int(time.time())

                tran.conn.insert(role_command, params)

                return admin_id
        except Exception as e:
            log.error('新增管理后台用户失败,错误是:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_result(status=APIStatus.InternalServerError, msg='服务器内部错误,新增管理后台用户失败'))


class RootRoleManagementModel(object):

    @staticmethod
    def get_role_list(cursor, params):
        fields = """
        tb_inf_roles.id,
        tb_inf_roles.`name` role_name,
        region_id,
        GROUP_CONCAT(tb_inf_pages.`name`) page_name
        """

        command = """
        SELECT
            {fields}
        FROM
            tb_inf_roles
            INNER JOIN tb_inf_role_pages ON tb_inf_role_pages.role_id = tb_inf_roles.id AND tb_inf_role_pages.is_deleted = 0
            INNER JOIN tb_inf_pages ON tb_inf_pages.id = tb_inf_role_pages.page_id AND tb_inf_pages.is_deleted = 0
        GROUP BY tb_inf_roles.id
        """

        count = cursor.query_one(command.format(fields="""COUNT(1) count"""))['count']

        command += """ LIMIT {0}, {1} """.format(params.get('page'), params.get('limit'))

        role_list = cursor.query(command.format(fields=fields))

        data = {
            'role_list': role_list if role_list else [],
            'count': count if count else 0
        }

        return data

    @staticmethod
    def post_data(cursor, params):
        try:
            with cursor.begin() as tran:
                role_sql = """
                INSERT INTO tb_inf_roles(name, comment, region_id) 
                VALUES(:role_name, :role_comment, :region_id)
                """

                role_id = tran.conn.insert(role_sql, params)

                # 为tb_inf_role_pages新增记录
                params['role_id'] = role_id
                params['create_time'] = int(time.time())
                params['update_time'] = int(time.time())
                for page_id in params['page_id_list']:
                    page_sql = """
                    INSERT INTO tb_inf_role_pages(role_id, page_id, create_time, update_time)
                    VALUES(:role_id, :page_id, :create_time, :update_time)
                    """
                    params['page_id'] = page_id

                    tran.conn.insert(page_sql, params)

                return role_id
        except Exception as e:
            log.error('添加角色失败,失败原因是:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_result(status=APIStatus.InternalServerError, msg='添加角色失败'))

    @staticmethod
    def put_data(cursor, params):
        try:
            if params.get('page_id_list'):
                page_id_list = params.pop('page_id_list')
            with cursor.begin() as tran:
                pass
        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_result(status=APIStatus.InternalServerError, msg='修改角色失败'))