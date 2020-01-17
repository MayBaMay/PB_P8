#! /usr/bin/env python3
# coding: utf-8

"""
This module manage insertion database.
"""
from django.db import IntegrityError
from foodSearch.models import Category, Product, Favorite


class DbInnit:
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
            try:
                product = Product.objects.create(
                    reference=prod['id'],
                    name=prod['product_name'],
                    url=prod['url'],
                    nutrition_grade_fr=prod['nutrition_grade_fr']
                )
                for category in prod['categories']:
                    try:
                        category_id = Category.objects.get(reference="category")
                        product.categories.add(category_id)
                    except Category.DoesNotExist:
                        pass
            except IntegrityError:
                pass


    def insert_prod_cat(self, data):
        """
        Insert links between products and category in table Asso_Prod_Cat
        """

        pass

if __name__ == "__main__":
    pass
