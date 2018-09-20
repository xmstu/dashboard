import time

from flask_restful import abort

from server import log
from server.status import HTTPStatus, make_resp, APIStatus


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
            LEFT JOIN tb_inf_admin_roles ON tb_inf_admin_roles.admin_id = tb_inf_admins.id AND tb_inf_admin_roles.is_deleted = 0
            LEFT JOIN tb_inf_roles ON tb_inf_roles.id = tb_inf_admin_roles.role_id AND tb_inf_roles.is_deleted = 0
        GROUP BY
            tb_inf_admins.id
        """

        count = cursor.query(command.format(fields="""COUNT(1) count"""))
        count = len(count)

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
                id role_id,
                `name`,
            CASE WHEN id IN (
                    SELECT
                        role_id 
                    FROM
                        tb_inf_admin_roles
                        INNER JOIN tb_inf_roles ON tb_inf_roles.id = tb_inf_admin_roles.role_id 
                        AND tb_inf_roles.is_deleted = 0 
                    WHERE
                        tb_inf_admin_roles.is_deleted = 0 
                        AND admin_id = %d 
                        ) THEN
                        1 ELSE 0 
                    END AS `status` 
                FROM
                    tb_inf_roles 
            WHERE
                tb_inf_roles.is_deleted = 0
            """ % admin_id
            role_list = cursor.query(cmd)
            return role_list
        except Exception as e:
            log.error('获取当前用户角色失败,失败原因是:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.BadRequest, msg='获取当前用户角色失败'))

    @staticmethod
    def put_data(cursor, params):
        try:
            admin_id = params.pop('admin_id', 0)
            role_id_set = set(params.pop('role_id', []))
            is_active = params.pop('is_active', 0)
            rowcount = 0
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

                    rowcount += tran.conn.update(command.format(update_sql=update_sql), args={"admin_id": admin_id})

                    if role_id_set:
                        # 查出所有当前用户的角色id
                        cur_role_id_list = tran.conn.query("""SELECT role_id, is_deleted FROM tb_inf_admin_roles WHERE admin_id = %d""" % admin_id)
                        relationship = {i["role_id"]: i["is_deleted"] for i in cur_role_id_list}
                        cur_role_id_set = {i['role_id'] for i in cur_role_id_list}

                        # 需要删除关联的role_id
                        needed_delete_set = cur_role_id_set - role_id_set
                        # 需要增加关联的role_id
                        needed_add_set = role_id_set - cur_role_id_set
                        # 需要将is_deleted更新为0的role_id
                        needed_update_set = role_id_set & cur_role_id_set

                        create_time = update_time = int(time.time())

                        if needed_delete_set:
                            del_sql = """
                            UPDATE tb_inf_admin_roles SET is_deleted = 1, update_time =:update_time  WHERE role_id = :role_id
                            """
                            for del_role_id in needed_delete_set:
                                if not relationship[del_role_id]:
                                    rowcount += tran.conn.update(del_sql, {"update_time": update_time, "role_id": del_role_id})

                        if needed_add_set:

                            add_sql = """
                                            INSERT INTO tb_inf_admin_roles
                                            (admin_id, role_id, create_time, update_time) 
                                            VALUES(:admin_id, :role_id, :create_time, :update_time)"""
                            add_params = {"admin_id": admin_id, "create_time": create_time, "update_time": update_time}
                            for add_role_id in needed_add_set:
                                add_params['role_id'] = add_role_id
                                rowcount += tran.conn.insert(add_sql, add_params)

                        if needed_update_set:
                            update_sql = """
                            UPDATE tb_inf_admin_roles SET is_deleted = 0, update_time =:update_time  WHERE role_id = :role_id
                            """
                            for update_role_id in needed_update_set:
                                if relationship[update_role_id]:
                                    rowcount += tran.conn.update(update_sql, {"update_time": update_time, "role_id": update_role_id})
                    return rowcount

        except Exception as e:
            log.error('更新用户失败,失败原因是:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='服务器内部错误,更新管理后台用户失败'))

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
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='服务器内部错误,删除管理后台用户失败'))

    @staticmethod
    def post_data(cursor, params):
        try:
            role_id_list = params.pop('role_id')
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

                row_id_sum = 0
                for role_id in role_id_list:
                    params['role_id'] = role_id
                    row_id_sum += tran.conn.insert(role_command, params)

                if admin_id and row_id_sum:
                    return admin_id + row_id_sum
                return 0
        except Exception as e:
            log.error('新增管理后台用户失败,错误是:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='服务器内部错误,新增管理后台用户失败'))


class RootRoleManagementModel(object):

    @staticmethod
    def get_role_list(cursor, params):
        fields = """
        type,
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
        WHERE tb_inf_roles.is_deleted = 0
        GROUP BY tb_inf_roles.id
        """

        count = cursor.query(command.format(fields="""COUNT(1)"""))
        count = len(count)
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
                INSERT INTO tb_inf_roles(`type`, `name`, comment, region_id) 
                VALUES(:type, :role_name, :role_comment, :region_id)
                """

                role_id = tran.conn.insert(role_sql, params)

                # 为role_pages中间表新增关联记录
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
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='添加角色失败'))

    @staticmethod
    def put_data(cursor, params):
        try:
            # 记录更新的次数
            row_count = 0
            update_role_sql = """id=id"""
            # 直接更新的字段
            svs_list = ('type', 'role_name', 'role_comment', 'region_id')
            for key, value in params.items():
                if key in svs_list and value and isinstance(value, int):
                    update_role_sql += ', {key} = {value}'.format(key=key, value=value)
                elif key in svs_list and value and isinstance(value, str):
                    key = key.split('_')[1]
                    update_role_sql += ", {key} = '{value}'".format(key=key, value=value)
            with cursor.begin() as tran:
                if params.get('page_id_list'):
                    page_id_set = set(params.pop('page_id_list'))
                    # 找出所有当前角色的权限页面id
                    role_page_sql = """
                    SELECT
                        page_id,
                        is_deleted
                    FROM
                        tb_inf_role_pages 
                    WHERE
                        tb_inf_role_pages.role_id = %d
                    """ % params['role_id']
                    role_page_id_list = cursor.query(role_page_sql)
                    relationship = {i["page_id"]: i["is_deleted"] for i in role_page_id_list}
                    role_page_id_set = {i['page_id'] for i in role_page_id_list}

                    # 要删除关联的page_id
                    needed_delete_set = role_page_id_set - page_id_set
                    # 要增加关联的page_id
                    needed_add_set = page_id_set - role_page_id_set
                    # 需要将is_deleted更新为0的page_id
                    needed_update_set = page_id_set & role_page_id_set

                    # 更新角色id与页面id的关联
                    if needed_delete_set:
                        delete_sql = """
                        UPDATE
                            tb_inf_role_pages
                            SET is_deleted = 1
                        WHERE page_id = %d AND role_id = %d;
                        """
                        for page_id in needed_delete_set:
                            if not relationship[page_id]:
                                row_count += tran.conn.update(delete_sql % (page_id, params['role_id']))
                    if needed_add_set:
                        insert_sql = """
                        INSERT INTO tb_inf_role_pages(role_id, page_id, create_time, update_time)
                        VALUES(%d, %d, %d, %d)
                        """
                        create_time = update_time = int(time.time())
                        for page_id in needed_add_set:
                            row_count += tran.conn.insert(insert_sql % (params['role_id'], page_id, create_time, update_time))
                    if needed_update_set:
                        update_role_page_sql = """
                       UPDATE
                           tb_inf_role_pages
                           SET is_deleted = 0
                       WHERE page_id = %d AND role_id = %d;
                           """
                        for page_id in needed_update_set:
                            if relationship[page_id]:
                                row_count += tran.conn.update(update_role_page_sql % (page_id, params['role_id']))

                # 更新角色
                command = """
                UPDATE tb_inf_roles SET {update_role_sql} WHERE id=:role_id
                """
                row_count += tran.conn.update(command.format(update_role_sql=update_role_sql), {'role_id': params['role_id']})
                return row_count
        except Exception as e:
            log.error('修改角色失败,失败原因是:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='修改角色失败'))

    @staticmethod
    def delete_data(cursor, params):
        try:
            with cursor.begin() as tran:
                del_role_cmd = """UPDATE tb_inf_roles SET is_deleted = 1 WHERE id =:role_id"""
                del_admin_role_cmd = """UPDATE tb_inf_admin_roles SET is_deleted = 1 WHERE role_id =:role_id"""
                del_role_cmd_rowcount = tran.conn.update(del_role_cmd, params)
                del_admin_role_cmd_rowcount = tran.conn.update(del_admin_role_cmd, params)
                if del_role_cmd_rowcount and del_admin_role_cmd_rowcount:
                    return del_role_cmd_rowcount + del_admin_role_cmd_rowcount
                return
        except Exception as e:
            log.error('删除角色失败,失败原因是:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='删除角色失败'))

    @staticmethod
    def get_role_pages(cursor, params):
        try:
            role_page_command = """
            SELECT
                tb_inf_pages.id page_id,
                `name`,
            CASE WHEN tb_inf_pages.id IN (
                    SELECT
                        tb_inf_pages.id page_id 
                    FROM
                        tb_inf_pages
                        INNER JOIN tb_inf_role_pages ON tb_inf_role_pages.page_id = tb_inf_pages.id 
                        AND tb_inf_role_pages.is_deleted = 0 
                    WHERE
                        tb_inf_pages.is_deleted = 0 
                        AND tb_inf_role_pages.role_id = :role_id 
                        ) THEN
                        1 ELSE 0 
                    END AS `status` 
                FROM
                    tb_inf_pages
                WHERE
                    tb_inf_pages.is_deleted = 0 
            GROUP BY
                tb_inf_pages.id;
            """

            role_page_list = cursor.query(role_page_command, params)

            return role_page_list
        except Exception as e:
            log.error('获取权限页面失败:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='获取权限页面失败'))


class RootPageManagementModel(object):

    @staticmethod
    def get_all_pages(cursor, params):
        try:
            fields = """
                tb_inf_pages.id page_id,
                tb_inf_pages.`name` page_name,
                tb_inf_pages.`comment` page_comment,
                tb_inf_pages.path page_path,
                tb_inf_menus.id menu_id,
                tb_inf_menus.`name` menu_name
            """
            command = """
            SELECT
                {fields}
            FROM
                tb_inf_pages
                INNER JOIN tb_inf_menus ON tb_inf_menus.id = tb_inf_pages.menu_id AND tb_inf_menus.is_deleted = 0
            WHERE
                tb_inf_pages.is_deleted = 0
            """
            count = cursor.query_one(command.format(fields="""COUNT(1) count"""))['count']

            command += """ LIMIT {0}, {1} """.format(params.get('page'), params.get('limit'))

            page_list = cursor.query(command.format(fields=fields))

            return page_list if page_list else [], count if count else 0
        except Exception as e:
            log.error('获取所有页面失败:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='获取所有页面失败'))

    @staticmethod
    def post_data(cursor, params):
        try:
            with cursor.begin() as tran:
                command = """
                INSERT INTO
                    tb_inf_pages(name, comment, path, menu_id, create_time, update_time)
                VALUES(:page_name, :page_comment, :page_path, :parent_menu_id, :create_time, :update_time)
                """
                params['create_time'] = params['update_time'] = int(time.time())
                page_id = tran.conn.insert(command, params)
                return page_id
        except Exception as e:
            log.error('添加页面失败:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='添加页面失败'))

    @staticmethod
    def put_data(cursor, params):
        try:
            update_page_sql = """id=id"""
            # 直接更新的字段
            svs_list = ('page_name', 'page_comment', 'page_path', 'parent_menu_id')
            for key, value in params.items():
                if key in svs_list and value and isinstance(value, int):
                    update_page_sql += ', {key} = {value}'.format(key='menu_id', value=value)
                elif key in svs_list and value and isinstance(value, str):
                    key = key.split('_')[1]
                    update_page_sql += ", {key} = '{value}'".format(key=key, value=value)
            update_page_sql += ", {key} = {value}".format(key='update_time', value=int(time.time()))
            command = """
            UPDATE tb_inf_pages SET {update_page_sql} WHERE id=:page_id
            """
            with cursor.begin() as tran:
                rowcount = tran.conn.update(command.format(update_page_sql=update_page_sql), {'page_id': params['page_id']})
                return rowcount
        except Exception as e:
            log.error('修改页面失败:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='修改页面失败'))

    @staticmethod
    def delete_data(cursor, params):
        try:
            with cursor.begin() as tran:
                command = """
                UPDATE tb_inf_pages SET is_deleted = 1 WHERE id=:page_id
                """
                return tran.conn.delete(command, params)
        except Exception as e:
            log.error('删除页面失败:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='删除页面失败'))

    @staticmethod
    def get_page_menus(cursor, params):
        try:
            page_menu_cmd = """
            SELECT
                tb_inf_menus.id
            FROM
                tb_inf_menus
                INNER JOIN tb_inf_pages ON tb_inf_pages.menu_id = tb_inf_menus.id AND tb_inf_pages.is_deleted = 0
            WHERE	
                tb_inf_menus.is_deleted = 0
                AND tb_inf_pages.id = :page_id;
            """
            all_menu_cmd = """
            SELECT
                id,
                `name`
            FROM
                tb_inf_menus
            WHERE
                tb_inf_menus.is_deleted = 0;
            """
            page_menu = cursor.query(page_menu_cmd, params)
            all_menu = cursor.query(all_menu_cmd)
            if params['page_id'] == 0:
                for detail in all_menu:
                    detail['status'] = 0
            else:
                page_menu_id_set = {i['id'] for i in page_menu}
                for detail in all_menu:
                    if detail['id'] in page_menu_id_set:
                        detail['status'] = 1
                    else:
                        detail['status'] = 0
            all_menu = [{i['name']: i['id'], 'status': i['status']} for i in all_menu]
            return all_menu

        except Exception as e:
            log.error('获取父菜单失败:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='获取父菜单失败'))


class RootMenuManagementModel(object):

    @staticmethod
    def get_all_menus(cursor, params):
        try:
            fields = """
                id,
                `name`,
                `comment`,
                page_id,
                parent_menu_id
            """
            cmd = """
            SELECT
                {fields}
            FROM
                `tb_inf_menus`
            WHERE tb_inf_menus.is_deleted = 0
            """

            count = cursor.query_one(cmd.format(fields="""COUNT(1) count"""))['count']

            cmd += """ LIMIT {0}, {1} """.format(params.get('page'), params.get('limit'))

            menu_list = cursor.query(cmd.format(fields=fields))

            data = {
                'menu_list': menu_list if menu_list else [],
                'count': count if count else 0
            }

            return data
        except Exception as e:
            log.error('获取所有菜单页面失败:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='获取所有菜单页面失败'))

    @staticmethod
    def post_data(cursor, params):
        try:
            with cursor.begin() as tran:

                command = """
                INSERT INTO tb_inf_menus(name, comment, page_id, parent_menu_id, create_time, update_time) 
                VALUES(:menu_name, :menu_comment, :page_id, :parent_menu_id, :create_time, :update_time);
                """
                params['create_time'] = int(time.time())
                params['update_time'] = int(time.time())

                menu_id = tran.conn.insert(command, params)

                return menu_id
        except Exception as e:
            log.error('添加菜单失败:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='添加菜单失败'))

    @staticmethod
    def put_data(cursor, params):
        try:
            menu_id = params.pop('menu_id')
            update_menu_sql = """id=id"""
            # 直接更新的字段
            svs_list = ('menu_name', 'menu_comment', 'page_id', 'parent_menu_id')
            for key, value in params.items():
                if key in svs_list and value and isinstance(value, int):
                    update_menu_sql += ', {key} = {value}'.format(key=key, value=value)
                elif key in svs_list and value and isinstance(value, str):
                    key = key.split('_')[1]
                    update_menu_sql += ", {key} = '{value}'".format(key=key, value=value)
            update_menu_sql += ", {key} = {value}".format(key='update_time', value=int(time.time()))
            command = """
                        UPDATE tb_inf_menus SET {update_menu_sql} WHERE id=:menu_id
                        """
            with cursor.begin() as tran:
                rowcount = tran.conn.update(command.format(update_menu_sql=update_menu_sql), {'menu_id': menu_id})
                return rowcount
        except Exception as e:
            log.error('修改菜单失败:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='修改菜单失败'))

    @staticmethod
    def delete_data(cursor, params):
        try:
            with cursor.begin() as tran:
                command = """
                UPDATE tb_inf_menus SET is_deleted = 1 WHERE id=:menu_id
                """
                return tran.conn.delete(command, params)
        except Exception as e:
            log.error('删除菜单失败:{}'.format(e))
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='删除菜单失败'))
