import os
import base64
from models.products import Pizza, Complement, Drink, Sauce, Package
from models.users import User, Administrator
from neomodel import db
from metrics import metrics_query_count, metrics_query_in_progress, metrics_query_latency
from cryptography.fernet import Fernet


class Catalog:
    @classmethod
    @db.transaction
    @metrics_query_latency.time()
    @metrics_query_in_progress.track_inprogress()
    def load_nodes(cls):
        # noinspection PyTypeChecker
        Pizza.create_or_update(
            {"name": "Crazy Crunch",
             "units": 1,
             "price": 99.9,
             "form": "REDONDA",
             "ingredients": ["QUESO",
                             "PEPPERONI",
                             "ORILLA DE CHICHARRÓN DE QUESO",
                             "PARMESANO"]},
            {"name": "Pepperoni Clásica",
             "units": 1,
             "price": 79.0,
             "form": "REDONDA",
             "ingredients": ["QUESO MOZZARELLA",
                             "QUESO MUENSTER",
                             "PEPPERONI"]},
            {"name": "3 MEAT TREAT",
             "units": 1,
             "price": 120,
             "form": "REDONDA",
             "ingredients": ["QUESO MOZZARELLA",
                             "QUESO MUENSTER",
                             "PEPPERONI",
                             "SALCHICHA ITALIANA",
                             "TOCINO"]},
            {"name": "ULTIMATE SUPREME",
             "units": 1,
             "price": 120,
             "form": "REDONDA",
             "ingredients": ["QUESO MOZZARELLA",
                             "QUESO MUENSTER",
                             "PEPPERONI",
                             "SALCHICHA ITALIANA",
                             "CHAMPIÑOES",
                             "CEBOLLA",
                             "PIMIENTOS VERDES"]},
            {"name": "HULA HAWAIIAN",
             "units": 1,
             "price": 120,
             "form": "REDONDA",
             "ingredients": ["QUESO MOZZARELLA",
                             "QUESO MUENSTER",
                             "PIÑA",
                             "JAMÓN"]},
            {"name": "QUESO",
             "units": 1,
             "price": 120,
             "form": "REDONDA",
             "ingredients": ["QUESO MOZZARELLA",
                             "QUESO MUENSTER"]},
            {"name": "DEEP!DEEP! DISH",
             "units": 1,
             "price": 120,
             "form": "CUADRADA",
             "ingredients": ["QUESO MOZZARELLA",
                             "QUESO MUENSTER",
                             "PEPPERONI",
                             "CRUJIENTE AJO"]})

        # noinspection PyTypeChecker
        Complement.create_or_update(
            {"name": "Crazy Bread Relleno",
             "units": 5,
             "price": 50,
             "description": "Palitos de Pan",
             "ingredients": ["MANTEQUILLA CON AJO",
                             "PARMESANO"]},
            {"name": "Crazy Bread",
             "units": 8,
             "price": 49,
             "description": "8 Palitos de Pan",
             "ingredients": ["AJO",
                             "MANTEQUILLA",
                             "QUESO PARMESANO",
                             "PAN"]},
            {"name": "ITALIAN CHEESE BREAD",
             "units": 10,
             "price": 52,
             "description": "10 piezas de pan recién horneado",
             "ingredients": ["MASA CRUJIENTE",
                             "QUESO MOZZARELLA",
                             "QUESO MUENSTER",
                             "CONDIMENTOS"]},
            {"name": "CAESAR WINGS",
             "units": 8,
             "price": 80,
             "description": "Alitas de Pollo",
             "ingredients": ["SALSA TIPO BUFFALO",
                             "SPICY BBQ",
                             "BBQ"]})

        # noinspection PyTypeChecker
        Drink.create_or_update(
            {
                "name": "Pepsi",
                "units": 1,
                "price": 18.00,
                "brand": "PEPSI",
                "litres": 2
            },
            {
                "name": "Mirinda",
                "units": 1,
                "price": 18.50,
                "brand": "PEPSI",
                "litres": 2
            },
            {
                "name": "Manzana",
                "units": 1,
                "price": 18.50,
                "brand": "PEPSI",
                "litres": 2
            },
            {
                "name": "Any",
                "units": 1,
                "price": 18,
                "brand": "PEPSI",
                "litres": 2
            }
        )

        # noinspection PyTypeChecker
        Sauce.create_or_update(
            {
                "name": "Crazy Sauce",
                "units": 1,
                "price": 10,
                "description": "red, 75ml"
            }
        )

        # noinspection PyTypeChecker
        Package.create_or_update(
            {"name": "Comida Completa",
             "units": 1,
             "price": 150,
             "pizzas": ["Pepperoni Clásica"],
             "complements": ["Crazy Bread"],
             "drinks": ["Any"],
             "sauces": ["Crazy Sauce"]},
            {"name": "Paquete Fiesta",
             "units": 1,
             "price": 200,
             "pizzas": ["Pepperoni Clásica"],
             "complements": ["Crazy Bread"],
             "drinks": ["Any"],
             "sauces": ["Crazy Sauce"]},
            {"name": "Crazy Combo",
             "units": 1,
             "price": 60,
             "pizzas": None,
             "complements": ["Crazy Bread"],
             "drinks": None,
             "sauces": ["Crazy Sauce"]},
            {"name": "Ultra Big",
             "units": 1,
             "price": 450,
             "pizzas": ["3 MEAT TREAT", "HULA HAWAIIAN"],
             "complements": ["Crazy Bread"],
             "drinks": ["Pepsi", "Mirinda", "Manzana"],
             "sauces": ["Crazy Sauce"]})

        metrics_query_count.labels(object='Catalog', method='load_nodes').inc()

    @classmethod
    @db.transaction
    @metrics_query_latency.time()
    @metrics_query_in_progress.track_inprogress()
    def load_relations(cls):
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

        tree_meat_treat = Pizza.find_by_name("3 MEAT TREAT")
        hula_hawaiian = Pizza.find_by_name("HULA HAWAIIAN")
        pepsi = Drink.find_by_name("Pepsi")
        mirinda = Drink.find_by_name("Mirinda")
        manzana = Drink.find_by_name("Manzana")

        pkg_fiesta = Package.find_by_name("Ultra Big")
        pkg_fiesta.rel_pizza.connect(tree_meat_treat, {'units': 2}).save()
        pkg_fiesta.rel_pizza.connect(hula_hawaiian, {'units': 2}).save()
        pkg_fiesta.rel_complement.connect(crazy_bread, {'units': 1}).save()
        pkg_fiesta.rel_drink.connect(pepsi, {'units': 1}).save()
        pkg_fiesta.rel_drink.connect(mirinda, {'units': 1}).save()
        pkg_fiesta.rel_drink.connect(manzana, {'units': 1}).save()
        pkg_fiesta.rel_sauce.connect(crazy_sauce, {'units': 4}).save()

        metrics_query_count.labels(object='Catalog', method='load_relations').inc()

    @classmethod
    @db.transaction
    @metrics_query_latency.time()
    @metrics_query_in_progress.track_inprogress()
    def load_users(cls):
        # Encrypted Secret files
        file_encryption_key = open('/run/secrets/encryption_key', 'rb')
        encryption_key = file_encryption_key.read()
        file_encryption_key.close()
        fer = Fernet(encryption_key)

        file_default_app_user_name = open('/run/secrets/default_app_user_name', 'rb')
        file_default_app_user_password = open('/run/secrets/default_app_user_password', 'rb')
        file_default_app_admin_name = open('/run/secrets/default_app_admin_name', 'rb')
        file_default_app_admin_password = open('/run/secrets/default_app_admin_password', 'rb')

        decrypted_default_app_user_name = fer.decrypt(file_default_app_user_name.read())
        decrypted_default_app_admin_name = fer.decrypt(file_default_app_admin_name.read())

        decoded_default_app_user_name = base64.b64decode(decrypted_default_app_user_name)
        decoded_default_app_admin_name = base64.b64decode(decrypted_default_app_admin_name)

        decoded_default_app_user_name = decoded_default_app_user_name.decode()
        decoded_default_app_admin_name = decoded_default_app_admin_name.decode()

        # noinspection PyTypeChecker
        User.get_or_create(
            {"name": decoded_default_app_user_name.strip(),
             "password": file_default_app_user_password.read().strip()})

        # noinspection PyTypeChecker
        Administrator.get_or_create(
            {"name": decoded_default_app_admin_name.strip(),
             "password": file_default_app_admin_password.read().strip()})

        file_default_app_user_name.close()
        file_default_app_user_password.close()
        file_default_app_admin_name.close()
        file_default_app_admin_password.close()

        metrics_query_count.labels(object='Catalog', method='load_users').inc()
