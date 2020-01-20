#! /usr/bin/env python3
# coding: utf-8
import json

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from django.db import transaction

from foodSearch.models import Category, Product, Favorite

import openfoodfacts

class Init_db:

    def __init__(self):
        self.page = 149 # page counter
        self.total_pages = 828# number of page wanted from the api
        self.success = 0
        self.failed = 0

    def reset_db(self):
        """Method clearing database"""
        Category.objects.all().delete()
        Favorite.objects.all().delete()
        Product.objects.all().delete()

    def load_datas(self):
        """method loading datas from api in the database"""

        while self.page <= self.total_pages:
            print("loading page "+ str(self.page))
            # use openfactfood api to load pages
            page_prods = openfoodfacts.products.get_by_facets(
                {'country': 'france'}, page=self.page, locale="fr"
            )

            for product in page_prods:
                try:
                    with transaction.atomic():
                        # print("---------", product["product_name"], " ", product["id"])
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
                        # print(product["categories_hierarchy"])
                        # insert each category in database only if products has categories infos(no keyerror in product['categories_hierarchy'])
                        try:
                            with transaction.atomic():
                                for category in product['categories_hierarchy']:
                                    # print("found categories")
                                    try:
                                        with transaction.atomic():
                                            # try to get the category in database
                                            cat = Category.objects.get(reference=category)
                                            print("{} category already in database".format(cat.reference))
                                    except Category.DoesNotExist:
                                        # if category doesn't exist yet, create one
                                        cat = Category.objects.create(reference = category)
                                        categ = Category.objects.get(reference=category)
                                        print("{} category not in database, {} created".format(cat.reference, categ))
                                    # in any case, add a relation between Category and Product
                                    cat.products.add(new_product)
                                    # print("relation category__product added")
                                    print("product : {} in database, reference {}".format(new_product.name, new_product.reference))
                        ###### only keep cleaned datas #######
                        except KeyError as e:
                            pass
                            # self.failed +=1
                            # print("KeyError")
                        except IntegrityError:
                            pass
                            # self.failed +=1
                            # print("IntegrityError")
                        except AttributeError:
                            pass
                            # self.failed +=1
                            # print("AttributeError")
                        except JSONDecodeError:
                            pass

                    # self.success +=1
                except:
                    pass
                    # print("pas de categories?")
                    # self.failed +=1
            print("\n")
            self.page += 1

class Command(BaseCommand):

    def handle(self, *args, **options):
        db = Init_db()
        db.reset_db()
        db.load_datas()
        self.stdout.write(self.style.SUCCESS("{} products in database".format(Product.objects.count())))
        self.stdout.write(self.style.SUCCESS("{} categories in database".format(Category.objects.count())))
        # self.stdout.write(self.style.SUCCESS("{} succes".format(db.success)))
        # self.stdout.write(self.style.SUCCESS("{} failed".format(db.failed)))
