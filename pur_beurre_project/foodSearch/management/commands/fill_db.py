#! /usr/bin/env python3
# coding: utf-8

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from foodSearch.models import Category, Product, Favorite

import openfoodfacts

class Init_db:

    def __init__(self):
        self.page = 1 # page counter
        self.total_pages = 1000 # number of page wanted from the api

    def reset_db(self):
        """Method clearing database"""
        Category.objects.all().delete()
        Favorite.objects.all().delete()
        Product.objects.all().delete()

    def load_datas(self):
        """method loading datas from api in the database"""

        while self.page < self.total_pages:
            print("loading page "+ str(self.page))
            # use openfactfood api to load pages
            page_prods = openfoodfacts.products.get_by_facets(
                {'country': 'france'}, page=self.page, locale="fr"
            )

            for product in page_prods:

                try:
                    # insert each product in database
                    new_product = Product.objects.create(
                        reference = product["id"],
                        name = product["product_name"],
                        nutrition_grade_fr = product["nutrition_grades"],
                        url = product["url"],
                        image_url = product["image_url"],
                        image_small_url = product["image_small_url"],
                    )
                    # insert each category in database
                    for category in product['categories']:
                        try:
                            # try to get the category
                            Category.objects.get(reference=category)
                        except Category.DoesNotExist:
                            # if category doesn't exist yet, create one
                            Category.objects.create(reference = category)
                        # in any case, add a relation between Category and Product
                        product.categories.add(category_id)

                except KeyError as e:
                    pass
                except IntegrityError:
                    pass
                except AttributeError:
                    pass

            self.page += 1

        print("{} products loaded".format(Product.objects.count()))
        print("{} categories loaded".format(Category.objects.count()))


class Command(BaseCommand):

    def handle(self, *args, **options):
        db = Init_db()
        db.reset_db()
        db.load_datas()
        self.stdout.write(self.style.SUCCESS('Successfully load products'))
