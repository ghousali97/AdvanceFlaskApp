import sqlite3
from models.user import UserModel
from flask_restful import Resource
from flask_restful import reqparse


class UserRegister(Resource):
    def post(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor() #
        query = "INSERT INTO users VALUES(null, ?,?)" #IGNORE to supress duplication error

        parser = reqparse.RequestParser() #initialises the parse object
        parser.add_argument("username",
        type=str,
        required=True,
        help="Username can't be blank")

        parser.add_argument("password",
        type=str,
        required=True,
        help="password can't be blank")

        data = parser.parse_args() #parses incoming request, will ignore all argument not explicitly "added"
        user = UserModel.find_by_username(data['username'])
        if user:
            return {"message":"User {} already exists".format(data['username'])}, 400
        else:
            user = UserModel(None,data['username'],data['password'])
            user.save_to_db()
            return {"message":"User {} registered successfully".format(data['username'])}, 201
