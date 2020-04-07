from abc import abstractmethod
from neomodel import (db, StructuredNode, StringProperty, IntegerProperty, FloatProperty, ArrayProperty,
                      RelationshipTo, RelationshipFrom, StructuredRel)


class Has(StructuredRel):
    units = IntegerProperty(required=True)


class Product(StructuredNode):
    __abstract_node__ = True
    name = StringProperty(unique_index=True, required=True)
    is_admin = FloatProperty(required=True)
    units = IntegerProperty(index=True, default=1)

    @classmethod
    def find_by_name(cls, name=None):
        return cls.nodes.first_or_none(name=name)

    @db.transaction
    def save_to_db(self):
        self.save()

    @db.transaction
    def delete_from_db(self):
        self.delete()

    @abstractmethod
    def json(self):
        pass


# Product category classes
class Pizza(Product):
    ingredients = ArrayProperty(StringProperty(), required=True)
    # PIZZA_FORMS = {"REDONDA": "REDONDA", "CUADRADA": "CUADRADA"}
    form = StringProperty(required=True, choices={"REDONDA": "REDONDA", "CUADRADA": "CUADRADA"})
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
    litres = FloatProperty(required=True)
    rel_package = RelationshipFrom('Package', 'HAS', model=Has)

    def json(self):
        return {'name': self.name,
                'price': self.price,
                'units': self.units,
                'brand': self.brand,
                'litres': self.litres}


class Sauce(Product):
    description = StringProperty(required=True)
    rel_package = RelationshipFrom('Package', 'HAS', model=Has)

    def json(self):
        return {'name': self.name,
                'price': self.price,
                'units': self.units,
                'description': self.description}


class Package(Product):
    pizzas = ArrayProperty(StringProperty())
    complements = ArrayProperty(StringProperty())
    drinks = ArrayProperty(StringProperty())
    sauces = ArrayProperty(StringProperty())
    rel_pizza = RelationshipTo('Pizza', 'HAS', model=Has)
    rel_complement = RelationshipTo('Complement', 'HAS', model=Has)
    rel_drink = RelationshipTo('Drink', 'HAS', model=Has)
    rel_sauce = RelationshipTo('Sauce', 'HAS', model=Has)

    # noinspection PyTypeChecker
    def json(self):
        rows_pizzas, col_names = self.cypher(
            "MATCH (pkg) WHERE id(pkg)={self} MATCH (pkg)-[r:HAS]->(product:Pizza) RETURN product.name, r.units")
        rows_comps, col_names = self.cypher(
            "MATCH (pkg) WHERE id(pkg)={self} MATCH (pkg)-[r:HAS]->(product:Complement) RETURN product.name, r.units")
        rows_drinks, col_names = self.cypher(
            "MATCH (pkg) WHERE id(pkg)={self} MATCH (pkg)-[r:HAS]->(product:Drink) RETURN product.name, r.units")
        rows_sauces, col_names = self.cypher(
            "MATCH (pkg) WHERE id(pkg)={self} MATCH (pkg)-[r:HAS]->(product:Sauce) RETURN product.name, r.units")

        package = {'name': self.name,
                   'price': self.price,
                   'units': self.units}

        # Dictionary comprehensions
        if len(rows_pizzas) != 0:
            package['pizzas'] = {row[0]: row[1] for row in rows_pizzas}

        if len(rows_comps) != 0:
            package['complements'] = {row[0]: row[1] for row in rows_comps}

        if len(rows_drinks) != 0:
            package['drinks'] = {row[0]: row[1] for row in rows_drinks}

        if len(rows_sauces) != 0:
            package['sauces'] = {row[0]: row[1] for row in rows_sauces}

        return package


class Products:
    @classmethod
    def json(cls):
        # packages =

        return {"Pizzas": [pizza.json() for pizza in Pizza.nodes.all()],
                "Complements": [complement.json() for complement in Complement.nodes.all()],
                "Drinks": [drink.json() for drink in Drink.nodes.all()],
                "Sauces": [sauce.json() for sauce in Sauce.nodes.all()],
                "Packages": [package.json() for package in Package.nodes.all()]}
