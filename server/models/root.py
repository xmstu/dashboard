class RootManagementModel(object):

    @staticmethod
    def get_data(cursor, params):

        command = """
        SELECT
            id,
            account,
            user_name,
            region_id
        FROM
            `tb_inf_city_manager`
        WHERE 
            is_deleted = 0
        LIMIT :page, :limit
        """

        kwargs = {
            'page': params.get('page'),
            'limit': params.get('limit'),
        }

        city_manager_list = cursor.query(command, kwargs)

        data = {
            'city_manager_list': city_manager_list
        }

        return data

    @staticmethod
    def put_data(cursor, params):
        fields = """"""

        which_table = """"""

        fetch_where = """"""

        command = """"""

        data = cursor.query(command)

        return data

    @staticmethod
    def delete_data(cursor, params):
        fields = """"""

        which_table = """"""

        fetch_where = """"""

        command = """"""

        data = cursor.query(command)

        return data

    @staticmethod
    def post_data(cursor, params):
        fields = """"""

        which_table = """"""

        fetch_where = """"""

        command = """"""

        data = cursor.query(command)

        return data