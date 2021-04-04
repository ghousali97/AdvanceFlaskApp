from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity #these are the functions we created
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList



app =Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #prevents the app from tracking the changes being made by SLQALCHAMY this prevents un necassary resource usage
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #tells SQL alchmet that data.db lives on the root folder of our app
app.secret_key = "key" #secret key that needs to be protected in future
jwt = JWT(app, authenticate, identity) #create /auth endpoint
                                    #when we call /auth we send it username and password which is passed to authenticate function
                                    #once authenticated JWT returns a JWT token in response to /authenticate
                                    #on subsequent requests JWT token is passed to identy which returns a user object.
                                    #auth request should have content-type JSON
@app.before_first_request
def create_table():
    db.create_all() #creates all the tables as spcified elsewhere in the program

api = Api(app) #Api works with resourcs and every resource has to be a class.




api.add_resource(Item, '/item/<string:name>') #binds the resource to a URL
api.add_resource(Store,'/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5002, debug=True)
