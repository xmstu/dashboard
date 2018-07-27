from server.utils.constant import vehicle_name_list


class UsualVehicleModel(object):

    @staticmethod
    def get_usual_vehicle_ids(cursor):
        vehicle_id_sql = """
        SELECT
            id,
            name 
        FROM
            shm_dictionary_items 
        WHERE
            NAME IN ( '小面包车', '中面包车', '小货车', '4.2米', '5.2米', '6.8米', '7.6米', '9.6米', '13米', '17.5米' ) 
            AND dictionary_id = 2 
            AND is_deleted = 0
        """

        vehicle_id_ret = cursor.query(vehicle_id_sql)

        ret = {i['name']: i['id'] for i in vehicle_id_ret}

        vehicle_id_list = [ret.get(i, 0) for i in vehicle_name_list]

        return vehicle_id_list
