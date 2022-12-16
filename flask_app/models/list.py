from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import user
DB = "acnh_schema"

class List:
    def __init__(self, list):
        self.id = list["id"]
        self.name = list["name"]
        self.comments = list["comments"]
        self.bug_or_fish = list["bug_or_fish"]

        self.created_at = list["created_at"]
        self.updated_at = list["updated_at"]

        self.user = None

    @classmethod
    def get_all_by_id(cls, user_id):
        data = {"id": user_id}

        # Gets all lists
        query = """SELECT * FROM lists
                    WHERE lists.user_id = %(id)s;"""

        results = connectToMySQL(DB).query_db(query,data)
        lists = []
        for list in results:
            lists.append( cls(list) )
        return lists
    
    @classmethod
    def get_by_id(cls, user_id):
        data = {"id": user_id}

        query = """SELECT lists.id, lists.created_at, lists.updated_at, name, comments, bug_or_fish,
                    users.id as user_id, first_name, last_name, email, users.created_at as uc, users.updated_at as uu 
                    FROM lists
                    JOIN users on users.id = lists.user_id
                    WHERE lists.id = %(id)s;"""

        result = connectToMySQL(DB).query_db(query,data)

        list = cls(result[0])

        return list


    @classmethod
    def create_list(cls, list_dict):
        #Must check to ensure new list is valid
        if not cls.validate_list(list_dict):
            return False
        
        query = """INSERT INTO lists (name, comments, bug_or_fish, user_id) 
                VALUES (%(name)s, %(comments)s, %(bug_or_fish)s, %(user_id)s);"""
        list_id = connectToMySQL(DB).query_db(query, list_dict)
        list = cls.get_by_id(list_id)

        return list

    @classmethod
    def update_list(cls, list_data):
        print(f"Before Update:{list_data}")
        if not cls.validate_list(list_data):
            return False

        query = """UPDATE lists
                SET name=%(name)s, comments =%(comments)s, bug_or_fish=%(bug_or_fish)s
                WHERE lists.id = %(id)s;"""

        result = connectToMySQL(DB).query_db(query,list_data)
        # updated_list = cls.get_by_id(list_data["id"])

        return result

    @classmethod
    def delete_list(cls, list_id):
        data = {"id": list_id}
        query = "DELETE FROM lists WHERE id = %(id)s;"
        connectToMySQL(DB).query_db(query,data)

        return list_id

    @staticmethod
    def validate_list(list_data):

        #Always set to True initially, then set to False in following conditionals
        valid = True

        if len(list_data["name"]) < 3:
            flash("Name field must be greater than 2 characters.")
            valid = False

        if len(list_data["comments"]) < 3:
            flash("Description field must be greater than 2 characters.")
            valid = False

        if "bug_or_fish" not in list_data:
            flash("Is this entry regarding a bug or a fish?")
            valid = False

        return valid