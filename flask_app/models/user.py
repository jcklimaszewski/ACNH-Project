from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
DB = "acnh_schema"

class User:
    def __init__(self,user):
        self.id = user["id"]
        self.first_name = user["first_name"]
        self.last_name = user["last_name"]
        self.email = user["email"]
        self.password = user["password"]
        self.created_at = user["created_at"]
        self.updated_at = user["updated_at"]

    @classmethod
    def get_by_id(cls, user_id):

        data = {"id": user_id}
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query,data)
        
        # Check for if no User was found
        if len(result) < 1:
            return False

        return cls(result[0])

    @classmethod
    def get_by_email(cls,email):
        data = {
            "email": email
        }
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query,data)

        # Check for if no email was found
        if len(result) < 1:
            return False

        return cls(result[0])
    
    @classmethod
    def get_all(cls):
        query = "SELECT * from users;"
        user_data = connectToMySQL(DB).query_db(query)

        #Loops through all entries found in users, appends to empty list, then returns that list
        users = []
        for user in user_data:
            users.append(cls(user))

        return users

    @classmethod
    #function to authenticate a user by input
    def authenticate_user(cls, input):
        
        valid = True
        existing_user = cls.get_by_email(input["email"])
        password_valid = True

        if not existing_user:
            valid = False
            
        else:
            password_valid = bcrypt.check_password_hash(existing_user.password, input['password'])
        
            if not password_valid:
                valid = False

        if not valid:
            flash("That email & password combination does not match our records.")
            return False

        return existing_user
    
    @classmethod
    def create_user(cls, user):

        # MUST validate user before creating entry!
        if not cls.validate_user(user):
            return False

        # Save User Password in a hash
        pw_hash = bcrypt.generate_password_hash(user['password'])
        user = user.copy()
        user["password"] = pw_hash

        query = """
                INSERT into users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
                """

        user_id = connectToMySQL(DB).query_db(query, user)
        new_user = cls.get_by_id(user_id)

        return new_user

    #User validation now stored in classmethod to check if email already exists in db
    @classmethod
    def validate_user(cls, user):
        valid = True

        if len(user["first_name"]) < 3:
            valid = False
            flash("First name must be greater than 2 characters")

        if len(user["last_name"]) < 3:
            valid = False
            flash("Last name must be greater than 2 characters") 

        if len(user["password"]) < 8:
            valid = False
            flash("Password must be at least 8 characters") 

        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address")
            valid = False

        if user["password"] != user["pw_confirm"]:
            flash("Could not confirm password. Both fields must match.")
            valid = False

        email_has_account = User.get_by_email(user["email"])
        if email_has_account:
            flash("An account with that email already exists, please log in.")
            valid = False

        return valid
    
