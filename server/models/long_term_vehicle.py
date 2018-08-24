class LongTermVehiclModel(object):

    @staticmethod
    def get_count(cursor):

        command = """
        SELECT
            count(1) count
        FROM
            `x_activity_inputs` 
        WHERE
            is_deleted = 0
            AND type = 140 
        """

        count = cursor.query_one(command)['count']

        return count

    @staticmethod
    def get_data(cursor, new_count):
        command = """
        SELECT
            content,
            create_time,
            update_time
        FROM
            `x_activity_inputs` 
        WHERE
            is_deleted = 0
            AND type = 140 
        ORDER BY id DESC
        LIMIT {new_count};
        """

        data = cursor.query(command.format(new_count=new_count))

        return data
