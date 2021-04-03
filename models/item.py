
from db import db
from .store import StoreModel
class ItemModel(db.Model):

    __tablename__ = 'items'

    #All database columns should be added here otherwise SQLAlchmey wont read / update them
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price = db.Column(db.Float(precision=2))
    #set store.id as foreign key => Under the hood SQL alchemy uses join statement
    #by design this should force that every item needs to have a valid store ID, however sqlite does not have
    #concept of foreign key and will allow the creation 
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel') #Tell SQL alchemy what a store is

    def __init__(self,name,price,store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name":self.name, "price":self.price, "sid":self.store_id}

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first() #filter by is query builder so it builds query automatically. The table is used from table name above.
                                                            #The data is converted to item model object.
    @classmethod
    def get_all(cls):
        return list(cls.query.all())

    def save_to_db(self):
        db.session.add(self) #SQLAlchmey knows how to convert from object to table rows
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
