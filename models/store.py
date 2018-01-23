from db import db

class StoreModel(db.Model):
  __tablename__ = 'stores'

  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(80))

  # list, signifies "many" in the relationship thingie
  # without lazy, we have a list and we save a query to db
  # but it's slower to create a store
  items = db.relationship('ItemModel', lazy = 'dynamic')  

  def __init__(self, name):
    self.name = name

  def json(self): # with lazy = dynamic, self.items is a query builder and needs ".all()"
    return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

  @classmethod
  def find_by_name(cls, name):
    return cls.query.filter_by(name = name).first()
  
  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()