import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    #All database columns should be added here otherwise SQLAlchmey wont read / update them
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    #the variable name above should match the ones below. SQL alchemy will use them and pump the values down immediately to initialise the object

    def __init__(self,_id,username,password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first()
        '''connection = sqlite3.connect('data.db')
        cursor = connection.cursor() #responsible for executing the queries and getting results
        query ="SELECT * FROM users WHERE username=?"
        result = cursor.execute(query,(username,)) #the second argument needs to be a tuple always so follow this syntax for single values
        row = result.fetchone() #returns the first row / result
        if row:
            user = cls(*row)# this means cls(row[0],row[1],row[2]) cls means current classs
        else:
            user = None
        connection.close()

        return user'''

    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()
        """connection = sqlite3.connect('data.db')
        cursor = connection.cursor() #responsible for executing the queries and getting results
        query ="SELECT * FROM users WHERE id=?"
        result = cursor.execute(query,(_id,)) #the second argument needs to be a tuple always so follow this syntax for single values
        row = result.fetchone() #returns the first row / result
        if row:
            user = cls(*row)# this means cls(row[0],row[1],row[2]) cls means current classs
        else:
            user = None
        connection.close()

        return user"""

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
