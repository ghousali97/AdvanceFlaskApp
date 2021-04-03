
from db import db

class StoreModel(db.Model):

    __tablename__ = 'stores'

    #All database columns should be added here otherwise SQLAlchmey wont read / update them
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    items = db.relationship('ItemModel', lazy='dynamic') #backward relationship to get the coreesponding items

    def __init__(self,name):
        self.name = name

    def json(self):
        return {"sid":self.id, "name":self.name, "items":[item.json() for item in self.items.all()]}

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
