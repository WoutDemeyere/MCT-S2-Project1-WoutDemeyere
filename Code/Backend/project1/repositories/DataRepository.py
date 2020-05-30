from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def update_ip(id, ip):
        sql = "UPDATE takel SET ip = %s WHERE takel_id = %s"
        params = [ip, id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_start_pos(id, pos):
        sql = "UPDATE takel SET start-pos = %s WHERE takel_id = %s"
        params = [pos, id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_end_pos(id, pos):
        sql = "UPDATE takel SET end-pos = %s WHERE takel_id = %s"
        params = [pos, id]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def update_curr_pos(id, pos):
        sql = "UPDATE takel SET curr_pos = %s WHERE takel_id = %s"
        params = [pos, id]
        return Database.execute_sql(sql, params)
