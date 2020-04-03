from models.products import Pizza, Complement, Drink, Sauce, Package
from neomodel import db


class Catalog:
    @classmethod
    @db.transaction
    def load(cls):
        Pizza(name="Crazy Crunch",
              units=1,
              price=99.9,
              form="REDONDA",
              ingredients=["QUESO",
                           "PEPPERONI",
                           "ORILLA DE CHICHARRÓN DE QUESO",
                           "PARMESANO"]).save()

        Pizza(name="Pepperoni Clásica",
              units=1,
              price=79.0,
              form="REDONDA",
              ingredients=["QUESO MOZZARELLA",
                           "QUESO MUENSTER",
                           "PEPPERONI"]).save()

        Pizza(name="3 MEAT TREAT",
              units=1,
              price=120,
              form="REDONDA",
              ingredients=["QUESO MOZZARELLA",
                           "QUESO MUENSTER",
                           "PEPPERONI",
                           "SALCHICHA ITALIANA",
                           "TOCINO"]).save()

        Pizza(name="ULTIMATE SUPREME",
              units=1,
              price=120,
              form="REDONDA",
              ingredients=["QUESO MOZZARELLA",
                           "QUESO MUENSTER",
                           "PEPPERONI",
                           "SALCHICHA ITALIANA",
                           "CHAMPIÑOES",
                           "CEBOLLA",
                           "PIMIENTOS VERDES"]).save()

        Pizza(name="HULA HAWAIIAN",
              units=1,
              price=120,
              form="REDONDA",
              ingredients=["QUESO MOZZARELLA",
                           "QUESO MUENSTER",
                           "PIÑA",
                           "JAMÓN"]).save()

        Pizza(name="QUESO",
              units=1,
              price=120,
              form="REDONDA",
              ingredients=["QUESO MOZZARELLA",
                           "QUESO MUENSTER"]).save()

        Pizza(name="DEEP!DEEP! DISH",
              units=1,
              price=120,
              form="CUADRADA",
              ingredients=["QUESO MOZZARELLA",
                           "QUESO MUENSTER",
                           "PEPPERONI",
                           "CRUJIENTE AJO"]).save()

        Complement(name="Crazy Bread Relleno",
                   units=5,
                   price=50,
                   description="Palitos de Pan",
                   ingredients=["MANTEQUILLA CON AJO",
                                "PARMESANO"]).save()

        Complement(name="Crazy Bread",
                   units=8,
                   price=49,
                   description="8 Palitos de Pan",
                   ingredients=["AJO",
                                "MANTEQUILLA",
                                "QUESO PARMESANO",
                                "PAN"]).save()

        Complement(name="ITALIAN CHEESE BREAD",
                   units=10,
                   price=52,
                   description="10 piezas de pan recién horneado",
                   ingredients=["MASA CRUJIENTE",
                                "QUESO MOZZARELLA",
                                "QUESO MUENSTER",
                                "CONDIMENTOS"]).save()

        Complement(name="CAESAR WINGS",
                   units=8,
                   price=80,
                   description="Alitas de Pollo",
                   ingredients=["SALSA TIPO BUFFALO",
                                "SPICY BBQ",
                                "BBQ"]).save()

        # noinspection PyTypeChecker
        Drink.get_or_create(
            {
                "name": "Pepsi",
                "units": 1,
                "price": 18.00,
                "brand": "PEPSI"
            },
            {
                "name": "Mirinda",
                "units": 1,
                "price": 18.50,
                "brand": "PEPSI"
            },
            {
                "name": "Manzana",
                "units": 1,
                "price": 18.50,
                "brand": "PEPSI"
            },
            {
                "name": "Any",
                "units": 1,
                "price": 18,
                "brand": "PEPSI"
            }
        )

        # noinspection PyTypeChecker
        Sauce.get_or_create(
            {
                "name": "Crazy Sauce",
                "units": 1,
                "price": 10,
                "description": "red, 75ml"
            }
        )

        Package(name="Comida Completa",
                units=1,
                price=150,
                pizzas=["Pepperoni Clásica"],
                complements=["Crazy Bread"],
                drinks=["Any"],
                sauces=["Crazy Sauce"]).save()

        Package(name="Paquete Fiesta",
                units=1,
                price=200,
                pizzas=["Pepperoni Clásica", "Pepperoni Clásica"],
                complements=["Crazy Bread"],
                drinks=["Any"],
                sauces=["Crazy Sauce"]).save()

        Package(name="Crazy Combo",
                units=1,
                price=60,
                pizzas=None,
                complements=["Crazy Bread"],
                drinks=None,
                sauces=["Crazy Sauce"]).save()

        pepperoni_clasica = Pizza.find_by_name("Pepperoni Clásica")
        crazy_bread = Complement.find_by_name("Crazy Bread")
        any_drink = Drink.find_by_name("Any")
        crazy_sauce = Sauce.find_by_name("Crazy Sauce")

        pkg_comida_completa = Package.find_by_name("Comida Completa")
        pkg_comida_completa.rel_pizza.connect(pepperoni_clasica, {'units': 1}).save()
        pkg_comida_completa.rel_complement.connect(crazy_bread, {'units': 1}).save()
        pkg_comida_completa.rel_drink.connect(any_drink, {'units': 1}).save()
        pkg_comida_completa.rel_sauce.connect(crazy_sauce, {'units': 1}).save()

        pkg_fiesta = Package.find_by_name("Paquete Fiesta")
        pkg_fiesta.rel_pizza.connect(pepperoni_clasica, {'units': 2}).save()
        pkg_fiesta.rel_complement.connect(crazy_bread, {'units': 1}).save()
        pkg_fiesta.rel_drink.connect(any_drink, {'units': 1}).save()
        pkg_fiesta.rel_sauce.connect(crazy_sauce, {'units': 1}).save()

        pkg_crazy_combo = Package.find_by_name("Crazy Combo")
        pkg_crazy_combo.rel_complement.connect(crazy_bread, {'units': 1}).save()
        pkg_crazy_combo.rel_sauce.connect(crazy_sauce, {'units': 1}).save()
