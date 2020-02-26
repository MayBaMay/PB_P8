#!/usr/bin/env python
from django.test import TestCase
from ..models import Category, Product, Favorite, User
from ..results_parser import ResultsParser


class FilterFoundSubstitutesTestCase(TestCase):

    def setUp(self):
        query_prod = Product.objects.create(name="tarte citron meringuée", formated_name="x", brands="x", formated_brands="x", reference="1", nutrition_grade_fr="E")

        #categories :
        cat1 = Category.objects.create(reference="en:biscuits-and-cakes")
        cat2 = Category.objects.create(reference="en:cakes")
        cat3 = Category.objects.create(reference="en:pies")
        cat4 = Category.objects.create(reference="en:sweet-pies")
        cat5 = Category.objects.create(reference="en:frozen-cakes-and-pastries")
        cat6 = Category.objects.create(reference="en:dairy-desserts")
        cat7 = Category.objects.create(reference="en:desserts")
        cat8 = Category.objects.create(reference="en:cheese")

        #categories of query_prod
        cat1.products.add(query_prod)
        cat2.products.add(query_prod)
        cat3.products.add(query_prod)
        cat4.products.add(query_prod)
        cat7.products.add(query_prod)

        prod2 = Product.objects.create(name="madeleines citron surgelées", reference="2", nutrition_grade_fr="C", formated_name="x", brands="x", formated_brands="x")
        cat1.products.add(prod2)
        cat2.products.add(prod2)
        cat5.products.add(prod2)

        prod3 = Product.objects.create(name="yaourt", reference="3", nutrition_grade_fr="A", formated_name="x", brands="x", formated_brands="x")
        cat6.products.add(prod3)
        cat7.products.add(prod3)

        prod4 = Product.objects.create(name="tarte citron bio sans sucre ajouté", reference="4", nutrition_grade_fr="B", formated_name="x", brands="x", formated_brands="x")
        cat1.products.add(prod4)
        cat2.products.add(prod4)
        cat3.products.add(prod4)
        cat4.products.add(prod4)
        cat7.products.add(prod4)

        prod5 = Product.objects.create(name="fromage de chèvre", reference="5", nutrition_grade_fr="D", formated_name="x", brands="x", formated_brands="x")
        cat8.products.add(prod5)

        prod6 = Product.objects.create(name="tarte pomme allégée", reference="6", nutrition_grade_fr="B", formated_name="x", brands="x", formated_brands="x")
        cat1.products.add(prod6)
        cat2.products.add(prod6)
        cat3.products.add(prod6)
        cat4.products.add(prod6)
        cat7.products.add(prod6)

        prod7= Product.objects.create(name="tarte poire", reference="7", nutrition_grade_fr="B", formated_name="x", brands="x", formated_brands="x")
        cat1.products.add(prod7)
        cat2.products.add(prod7)
        cat3.products.add(prod7)
        cat4.products.add(prod7)
        cat7.products.add(prod7)

        prod8 = Product.objects.create(name="charlotte pomme citron", reference="8", nutrition_grade_fr="B", formated_name="x", brands="x", formated_brands="x")
        cat1.products.add(prod8)
        cat2.products.add(prod8)
        cat3.products.add(prod8)
        cat4.products.add(prod8)
        cat7.products.add(prod8)

        prod9 = Product.objects.create(name="roulé au citron", reference="9", nutrition_grade_fr="B", formated_name="x", brands="x", formated_brands="x")
        cat1.products.add(prod9)
        cat2.products.add(prod9)
        cat3.products.add(prod9)
        cat4.products.add(prod9)
        cat7.products.add(prod9)

    def test_products_same_categories(self):
        query_prod = Product.objects.get(reference="1")
        prod2 = Product.objects.get(reference="2")
        prod3 = Product.objects.get(reference="3")
        prod4 = Product.objects.get(reference="4")
        prod6 = Product.objects.get(reference="6")
        prod7 = Product.objects.get(reference="7")
        prod8 = Product.objects.get(reference="8")
        prod9 = Product.objects.get(reference="9")
        cat1 = Category.objects.get(reference="en:biscuits-and-cakes")
        cat2 = Category.objects.get(reference="en:cakes")
        cat3 = Category.objects.get(reference="en:pies")
        cat4 = Category.objects.get(reference="en:sweet-pies")
        cat5 = Category.objects.get(reference="en:frozen-cakes-and-pastries")
        cat6 = Category.objects.get(reference="en:dairy-desserts")
        cat7 = Category.objects.get(reference="en:desserts")
        parser = ResultsParser(query_prod.id)
        self.assertEqual({'id':prod2.id, 'nb':2, 'cats_list':[cat1, cat2]} in parser.all_results, True)
        self.assertEqual( {'id':prod4.id, 'nb':5, 'cats_list':[cat1, cat2, cat3, cat4, cat7]} in parser.all_results, True)
        self.assertEqual( {'id':prod3.id, 'nb':1, 'cats_list':[cat7]} in parser.all_results, True)
        self.assertEqual( {'id':prod6.id, 'nb':5, 'cats_list':[cat1, cat2, cat3, cat4, cat7]} in parser.all_results, True)
        self.assertEqual( {'id':prod7.id, 'nb':5, 'cats_list':[cat1, cat2, cat3, cat4, cat7]} in parser.all_results, True)
        self.assertEqual( {'id':prod8.id, 'nb':5, 'cats_list':[cat1, cat2, cat3, cat4, cat7]} in parser.all_results, True)
        self.assertEqual( {'id':prod9.id, 'nb':5, 'cats_list':[cat1, cat2, cat3, cat4, cat7]} in parser.all_results, True)

    def test_get_most_relevant_products(self):
        query_prod = Product.objects.get(reference="1")
        prod2 = Product.objects.get(reference="2")
        prod3 = Product.objects.get(reference="3")
        prod4 = Product.objects.get(reference="4")
        prod6 = Product.objects.get(reference="6")
        prod7 = Product.objects.get(reference="7")
        prod8 = Product.objects.get(reference="8")
        prod9 = Product.objects.get(reference="9")
        parser = ResultsParser(query_prod.id)
        ids=[]
        for elt in parser.get_most_relevant_products():
            ids.append(elt['id'])
        self.assertEqual(ids, [prod4.id, prod6.id, prod7.id, prod8.id, prod9.id, prod2.id, prod3.id])

    def test_get_results_queryset(self):
        query_prod = Product.objects.get(reference="1")
        parser = ResultsParser(query_prod.id)
        self.assertEqual(parser.relevant_results_queryset.count(), 7)
        result_list = []
        for elt in parser.relevant_results_queryset:
            result_list.append((elt.reference, elt.nutrition_grade_fr))
        self.assertEqual(result_list, [("3", "A"), ("4", "B"), ("6", "B"), ("9", "B"), ("7", "B"), ("8", "B"),("2", "C")])

    def test_get_results_dict_with_favorite_info(self):
        query_prod = Product.objects.get(reference="1")
        user = User.objects.create(username="test User")
        prod2 = Product.objects.get(reference="2")
        prod3 = Product.objects.get(reference="3")
        prod4 = Product.objects.get(reference="4")
        prod6 = Product.objects.get(reference="6")
        prod7 = Product.objects.get(reference="7")
        prod8 = Product.objects.get(reference="8")
        prod9 = Product.objects.get(reference="9")
        Favorite.objects.create(user=user, substitute=prod4, initial_search_product=query_prod)
        parser = ResultsParser(query_prod.id)
        self.assertEqual(parser.results_infos, [
                                                {prod3: False},
                                                {prod4: True},
                                                {prod6: False},
                                                {prod9: False},
                                                {prod7: False},
                                                {prod8: False},
                                                {prod2: False}
                                                ])

    def test_paginator(self):
        query_prod = Product.objects.get(reference="1")
        user = User.objects.create(username="test User")
        prod2 = Product.objects.get(reference="2")
        prod3 = Product.objects.get(reference="3")
        prod4 = Product.objects.get(reference="4")
        Favorite.objects.create(user=user, substitute=prod4, initial_search_product=query_prod)
        parser = ResultsParser(query_prod.id)
        self.assertEqual(parser.paginator(1)[0], {prod3:False})