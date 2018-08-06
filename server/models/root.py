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