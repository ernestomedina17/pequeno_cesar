from neomodel import (db, StructuredNode, StringProperty, IntegerProperty, FloatProperty, ArrayProperty,
                      RelationshipTo, RelationshipFrom, StructuredRel)


class Has(StructuredRel):
    units = IntegerProperty(required=True)


class Product(StructuredNode):
    __abstract_node__ = True
    name = StringProperty(unique_index=True, required=True)
    price = FloatProperty(required=True)
    units = IntegerProperty(index=True, default=1)

    @classmethod
    def find_by_name(cls, name):
        return cls.nodes.first_or_none(name=name)

    @db.transaction
    def save_to_db(self):
        self.save()

    @db.transaction
    def delete_from_db(self):
        self.delete()


# Product category classes
class Pizza(Product):
    ingredients = ArrayProperty(StringProperty(), required=True)
    PIZZA_FORMS = {"REDONDA": "REDONDA", "CUADRADA": "CUADRADA"}
    form = StringProperty(required=True, choices=PIZZA_FORMS)
    rel_package = RelationshipFrom('Package', 'HAS', model=Has)

    def json(self):
        return {'name': self.name,
                'price': self.price,
                'units': self.units,
                'ingredients': [ingredient for ingredient in self.ingredients],
                'form': self.form}


class Complement(Product):
    description = StringProperty(required=True)
    ingredients = ArrayProperty(StringProperty(), required=True)
    rel_package = RelationshipFrom('Package', 'HAS', model=Has)

    def json(self):
        return {'name': self.name,
                'price': self.price,
                'units': self.units,
                'ingredients': [ingredient for ingredient in self.ingredients],
                'description': self.description}


class Drink(Product):
    brand = StringProperty(required=True)
    rel_package = RelationshipFrom('Package', 'HAS', model=Has)


class Sauce(Product):
    description = StringProperty(required=True)
    rel_package = RelationshipFrom('Package', 'HAS', model=Has)


class Package(Product):
    pizzas = ArrayProperty(StringProperty())
    complements = ArrayProperty(StringProperty())
    drinks = ArrayProperty(StringProperty())
    sauces = ArrayProperty(StringProperty())
    rel_pizza = RelationshipTo('Pizza', 'HAS', model=Has)
    rel_complement = RelationshipTo('Complement', 'HAS', model=Has)
    rel_drink = RelationshipTo('Drink', 'HAS', model=Has)
    rel_sauce = RelationshipTo('Sauce', 'HAS', model=Has)




#class Products:
#    @classmethod
#    def json(cls):
#        return {"products": [product.json() for product in Product.nodes.all()]}
