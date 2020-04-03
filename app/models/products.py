from neomodel import (db, StructuredNode, StringProperty, IntegerProperty, FloatProperty, ArrayProperty,
                      RelationshipTo, RelationshipFrom)
from models.relationships import HasPizzaRel, HasComplementRel, HasDrinkRel, HasSauceRel

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
    form = StringProperty(required=False, choices={'R': 'REDONDA', 'C': 'CUADRADA'}, default='R')
    rel_package = RelationshipFrom('Package', 'HAS', cardinality='ZeroOrMore', model=HasPizzaRel)

    def json(self):
        return {'name': self.name,
                'price': self.price,
                'units': self.units,
                'ingredients': [ingredient for ingredient in self.ingredients],
                'form': self.form}


class Complement(Product):
    description = StringProperty(required=True)
    ingredients = ArrayProperty(StringProperty(), required=True)
    rel_package = RelationshipFrom('Package', 'HAS', cardinality='ZeroOrMore', model=HasComplementRel)

    def json(self):
        return {'name': self.name,
                'price': self.price,
                'units': self.units,
                'ingredients': [ingredient for ingredient in self.ingredients],
                'description': self.description}


class Drink(Product):
    brand = StringProperty(required=True)
    rel_package = RelationshipFrom('Package', 'HAS', cardinality='ZeroOrMore', model=HasDrinkRel)


class Sauce(Product):
    description = StringProperty(required=True)
    rel_package = RelationshipFrom('Package', 'HAS', cardinality='ZeroOrMore', model=HasSauceRel)


class Package(Product):
    pizzas = ArrayProperty(StringProperty())
    complements = ArrayProperty(StringProperty())
    drinks = ArrayProperty(StringProperty())
    sauces = ArrayProperty(StringProperty())
    rel_pizza = RelationshipTo('Pizza', 'HAS', cardinality='ZeroOrMore', model=HasPizzaRel)
    rel_complement = RelationshipTo('Complement', 'HAS', cardinality='ZeroOrMore', model=HasComplementRel)
    rel_drink = RelationshipTo('Drink', 'HAS', cardinality='ZeroOrMore', model=HasDrinkRel)
    rel_sauce = RelationshipTo('Sauce', 'HAS', cardinality='ZeroOrMore', model=HasSauceRel)


#class Products:
#    @classmethod
#    def json(cls):
#        return {"products": [product.json() for product in Product.nodes.all()]}
