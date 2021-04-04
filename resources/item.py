from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
import sqlite3
import itertools



class Item(Resource):
    @jwt_required() #mandates having a valid JWT token in request otherwise 401 response will be given. The request should have header Audthorisation with value JWT <token>
    def get(self,name): #this means the student resource can only be accessed by get method.
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        else:
            return {"item":[]}, 404

        """connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * from items WHERE name=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"item":{"name":row[1],"price":row[2]}}, 200
        else:
            return {"item":[]}, 404
"""

    def post(self,name):

        parser = reqparse.RequestParser() #initialises the parse object
        parser.add_argument("name",
        type=str,
        required=True,
        help="Item name can't be blank")

        parser.add_argument("price",
        type=float,
        required=True,
        help="Price can't be blank")

        parser.add_argument("sid",
        type=int,
        required=True,
        help="Store can't be blank")

        data = parser.parse_args()

        item = ItemModel.find_by_name(data['name'])
        if item:
            return {"message":"Item {} already exists".format(data["name"])}, 400
        else:
            item = ItemModel(data['name'],data['price'],data['sid'])
            item.save_to_db()
            return item.json(), 201
        """connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT OR IGNORE INTO items VALUES(null, ?, ?) "#or ignore supress the unique name violation allowing us ot handle error gracefully

        cursor.execute(query,(data['name'],data['price']))
        connection.commit()
        connection.close()

        if cursor.rowcount == 1:
            new_item = {"name":data['name'],
                        "price":data['price']}
            return {"item":new_item}, 201
        else:
            return {"message":"Item {} already exists".format(data["name"])}, 400
        """


    def put(self,name):
        parser = reqparse.RequestParser() #initialises the parse object
        parser.add_argument("price",
        type=float,
        required=True,
        help="This field can't be blank")

        parser.add_argument("name",
        type=str,
        required=True,
        help="This field can't be blank")

        parser.add_argument("sid",
        type=int,
        required=True,
        help="Store can't be blank")

        data = parser.parse_args() #parses incoming request, will ignore all argument not explicitly "added"

        item = ItemModel.find_by_name(data['name'])
        if item:
            item.price = data['price']

        else:
            item = ItemModel(data['name'],data['price'],data['sid'])
            try:
                item.save_to_db()
            except:
                return { "message":"Store with ID {} does not exist".format(data['sid'])}, 400
                }
        return item.json(),200

        """connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        0query = "REPLACE INTO items VALUES(null, ?, ?) " #Replace updates the remaining values when there is a unique clash
        #Alternately "UPDATE items SET price = ? WHERE name = ?"

        cursor.execute(query,(data['name'],data['price']))
        connection.commit()
        connection.close()


        if cursor.rowcount == 1:
            new_item = {"name":data['name'],
                    "price":data['price']}
            return new_item, 200
        else:
            return {"message":"Insertion failed!"}, 400
"""
    def delete(self,name):


        parser = reqparse.RequestParser() #initialises the parse object

        parser.add_argument("name",
        type=str,
        required=True,
        help="Item name can't be blank")

        data = parser.parse_args()

        item = ItemModel.find_by_name(data['name'])
        if item:
            item.delete_from_db()
            return  {"message":"Item {} removed successfully".format(data['name'])},200
        else:
            return {"message":"Item does not exist"}, 404




        """query = "DELETE FROM items where name = ?"

        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            result = cursor.execute(query,(data['name'],))

            connection.commit()
            connection.close()
            if result.rowcount >= 1:
                return  {"message":"Item {} removed successfully".format(data['name'])},200
            else:
                return {"message":"Item does not exist"}, 404
        except:
            return {"message":"Database error occured"},500"""

class ItemList(Resource):
    def get(self):
        return {"items":[x.json() for x in ItemModel.get_all()]}, 200
        #item_list = []
        #for item in items:
        #    item_list.append({"name":item.name, "price":item.price})
        #return {"items":item_list}, 200

        """connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * from items"
        cursor.execute(query)
        #results = cursor.execute(query) #this will only return the values so your reults won't have keys like "namr"
        #return {"items":list(results.fetchall())}, 200

        desc = cursor.description #gets all the column names from the respnse
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row)) #sets column name as key for all retrned valued
            for row in cursor.fetchall()]
        return {"items":data}, 200"""
