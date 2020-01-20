#! /usr/bin/env python3
# coding: utf-8
import json
import time
from statistics import mean

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from django.db import transaction

from foodSearch.models import Category, Product, Favorite

import openfoodfacts

class Init_db:

    def __init__(self):
        self.page = 601 # page counter
        self.total_pages = 1000 # number of page wanted from the api
        self.tps = []

    def reset_db(self):
        """Method clearing database"""
        Category.objects.all().delete()
        Favorite.objects.all().delete()
        Product.objects.all().delete()

    def load_datas(self):
        """method loading datas from api in the database"""

        while self.page <= self.total_pages:
            print("\n")
            print("loading page "+ str(self.page))
            start_time = time.time()
            # use openfactfood api to load pages
            page_prods = openfoodfacts.products.get_by_facets(
                {'country': 'france'}, page=self.page, locale="fr"
            )

            for product in page_prods:
                try:
                    with transaction.atomic():
                        # insert each product in database
                        categories = product["categories_hierarchy"]
                        new_product = Product.objects.create(
                            reference = product["id"],
                            name = product["product_name"],
                            nutrition_grade_fr = product["nutrition_grades"],
                            url = product["url"],
                            image_url = product["image_url"],
                            image_small_url = product["image_small_url"],
                        )
                        # insert each category in database only if products has categories infos(no keyerror in product['categories_hierarchy'])
                        try:
                            with transaction.atomic():
                                for category in product['categories_hierarchy']:
                                    if category[0:3] == 'en:':
                                        try:
                                            with transaction.atomic():
                                                # try to get the category in database
                                                cat = Category.objects.get(reference=category)
                                        except Category.DoesNotExist:
                                            # if category doesn't exist yet, create one
                                            cat = Category.objects.create(reference = category)
                                            categ = Category.objects.get(reference=category)
                                        # in any case, add a relation between Category and Product
                                        cat.products.add(new_product)
                        ###### only keep cleaned datas #######
                        except KeyError as e:
                            pass
                        except IntegrityError:
                            pass
                        except AttributeError:
                            pass
                        except JSONDecodeError:
                            pass
                except:
                    pass

            tps_page = round((time.time() - start_time),1)
            print("Temps d'execution page: {} secondes ---".format(tps_page))
            self.tps.append(tps_page)
            self.page += 1

class Command(BaseCommand):

    def handle(self, *args, **options):
        db = Init_db()
        # db.reset_db()
        db.load_datas()
        self.stdout.write(self.style.SUCCESS("{} products in database".format(Product.objects.count())))
        self.stdout.write(self.style.SUCCESS("{} categories in database".format(Category.objects.count())))
        self.stdout.write(self.style.SUCCESS("Temps moyen d'execution : {} secondes ---".format(round(mean(db.tps),1))))
