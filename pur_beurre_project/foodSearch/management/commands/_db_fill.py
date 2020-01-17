#! /usr/bin/env python3
# coding: utf-8

"""
This module manage insertion database.
"""
from foodSearch.models import Category, Product, Favorite


class DbFill:
    """
    Insert data in MySQL database.
    """

    def __init__(self):
        self.delete_db()

    def delete_db(self):
    """Function used to clear database
    Django webSite models used : Product, Category, Favorite
    """
    Category.objects.all().delete()
    Favorite.objects.all().delete()
    Product.objects.all().delete()

    def insert_categories(self, categrories):
        """
        Insert categories in table Categories
        """
        for category in categrories:
            Category.objects.create(
                reference=category['id'],
                name=category['name'],
                url=category['url'],
                nb_products=category['products']
            )

    def insert_products(self, products):
        """
        insert products in table Produits
        """

        for prod in products:
            Product.objects.create(
                reference=prod['id'],
                name=prod['name'],
                url=prod['url'],
                nb_products=prod['products']
            )


    def insert_prod_cat(self, data):
        """
        Insert links between products and category in table Asso_Prod_Cat
        """

        pass

if __name__ == "__main__":
    pass
