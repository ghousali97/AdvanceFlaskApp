from models.store import StoreModel
from flask_restful import Resource
from flask_restful import reqparse


class Store(Resource):
    def get(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        else:
            return {"messaage":"Store {} does not exist".format(name)}, 404


    def post(self,name):
        parser = reqparse.RequestParser() #initialises the parse object
        parser.add_argument("name",
        type=str,
        required=True,
        help="Store name can't be blank")
        data = parser.parse_args()
        store = StoreModel.find_by_name(data['name'])
        if store:
            return {"message":"Store {} already exists".format(data["name"])}, 400
        else:
            store = StoreModel(data['name'])
            store.save_to_db()
            return store.json(), 201

    def delete(self, name):
        parser = reqparse.RequestParser() #initialises the parse object
        parser.add_argument("name",
        type=str,
        required=True,
        help="Store name can't be blank")
        data = parser.parse_args()
        store = StoreModel.find_by_name(data['name'])

        if store:
            store.delete_from_db()
            return {"message":"Store {} deleted successfully".format(data['name'])}, 200
        else:
            return {"messaage":"Store {} does not exist".format(data['name'])}, 404


class StoreList(Resource):
    def get(self):
        return {"stores":[x.json() for x in StoreModel.get_all()]}, 200
