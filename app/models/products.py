from neomodel import db, config, StructuredNode, StringProperty, IntegerProperty, FloatProperty

config.DATABASE_URL = 'bolt://neo4j:qwerty99@localhost:7687'


class Product(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    price = FloatProperty(required=True)
    CATEGORIES = {'Pizza': 'Pizza', 'Complement': 'Complement', 'Drink': 'Drink'}
    category = StringProperty(required=True, choices=CATEGORIES)
    units = IntegerProperty(index=True, default=1)

    def json(self):
        return {'name': self.name, 'price': self.price, 'category': self.category, 'units': self.units}

    @classmethod
    def find_by_name(cls, name):
        return cls.nodes.first_or_none(name=name)

    @db.transaction
    def save_to_db(self):
        self.save()

    @db.transaction
    def delete_from_db(self):
        self.delete()
