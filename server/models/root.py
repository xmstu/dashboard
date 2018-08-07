class RootManagementModel(object):

    @staticmethod
    def get_data(cursor, params):

        fields = """
        id,
        account,
        user_name,
        region_id
        """

        command = """
        SELECT
            {fields}
        FROM
            `tb_inf_city_manager`
        WHERE 
            is_deleted = 0
        """

        count = cursor.query_one(command.format(fields="""COUNT(1) count"""))

        command += """ LIMIT {0}, {1} """.format(params.get('page'), params.get('limit'))

        city_manager_list = cursor.query(command.format(fields=fields))

        data = {
            'city_manager_list': city_manager_list if city_manager_list else [],
            'count': count if count else 0
        }

        return data

    @staticmethod
    def put_data(cursor, params):
        update_sql = """id=id"""

        user_id = params.pop('user_id', 0)
        if user_id:
            update_list = (', {0}={1}'.format(key, "'" + value + "'" if isinstance(value, str) else value) for key, value in params.items() if value)
            for i in update_list:
                update_sql += i
            command = """
            UPDATE tb_inf_city_manager
            SET {update_sql}
            WHERE is_deleted = 0 AND id=:user_id
            """

            rowcount = cursor.update(command.format(update_sql=update_sql), args={"user_id": user_id})

            return rowcount
        else:
            return 0

    @staticmethod
    def delete_data(cursor, params):

        command = """
        UPDATE tb_inf_city_manager
        SET is_deleted = 1
        WHERE id=:user_id
        """

        rowcount = cursor.update(command, params)

        return rowcount

    @staticmethod
    def post_data(cursor, params):

        command = """
        INSERT INTO tb_inf_city_manager(account, password, user_name, avatar_url, region_id) 
        VALUES(:account, :password, :user_name, :avatar_url, :region_id)
        """

        params['avatar_url'] = 'https://mp.huitouche.com/static/images/newicon.png'

        user_id = cursor.insert(command, params)

        return user_id
