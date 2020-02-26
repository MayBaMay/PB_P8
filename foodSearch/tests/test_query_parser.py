#!/usr/bin/env python
from django.test import TestCase
from ..models import Category, Favorite, Product
from ..query_parser import QueryParser

class FilterFoundProductsTestCase(TestCase):

    def setUp(self):
        Product.objects.create(name="Fàke product for db", formated_name="FAKE PRODUCT FOR DB", brands="brand fake", formated_brands="BRAND FAKE", reference="1")
        Product.objects.create(name="Second fake prôduct", formated_name="SECOND FAKE PRODUCT", brands="the wrong one", formated_brands="THE WRONG ONE", reference="2")
        Product.objects.create(name="product", formated_name="PRODUCT", brands="not bad", formated_brands="NOT BAD", reference="3")
        self.query_name = "fàke product"
        self.query_name_brands = "fake prôduct brand"
        self.one_result_query = "Sécond"

    def test_split_upper_no_accent(self):
        parser = QueryParser(self.query_name_brands)
        self.assertEqual(parser.split_upper_no_accent(self.query_name_brands), ['FAKE', 'PRODUCT', 'BRAND'])
        parser = QueryParser(self.one_result_query)
        self.assertEqual(parser.split_upper_no_accent(self.one_result_query), ['SECOND'])

    def test_products_with_words(self):
        parser = QueryParser(self.query_name)
        self.assertEqual(parser.products_with_words().count(), 3)
        parser = QueryParser(self.query_name_brands)
        self.assertEqual(parser.products_with_words().count(), 3)
        parser = QueryParser(self.one_result_query)
        self.assertEqual(parser.products_with_words().count(), 1)

    def test_products_infos(self):
        parser = QueryParser(self.query_name)
        self.assertEqual(parser.products_infos()['1'], ["FAKE", "PRODUCT", "FOR", "DB", "BRAND", "FAKE"])
        self.assertEqual(parser.products_infos()['2'], ["SECOND", "FAKE", "PRODUCT", "THE", "WRONG", "ONE"])
        self.assertEqual(parser.products_infos()['3'], ["PRODUCT", "NOT", "BAD"])
        parser = QueryParser(self.query_name_brands)
        self.assertEqual(parser.products_infos()['1'], ["FAKE", "PRODUCT", "FOR", "DB", "BRAND", "FAKE"])
        self.assertEqual(parser.products_infos()['2'], ["SECOND", "FAKE", "PRODUCT", "THE", "WRONG", "ONE"])
        self.assertEqual(parser.products_infos()['3'], ["PRODUCT", "NOT", "BAD"])
        parser = QueryParser(self.one_result_query)
        self.assertEqual(parser.products_infos()['2'], ["SECOND", "FAKE", "PRODUCT", "THE", "WRONG", "ONE"])

    def test_occurences(self):
        parser = QueryParser(self.query_name)
        self.assertEqual(parser.occurences()['1'], 2)
        self.assertEqual(parser.occurences()['2'], 2)
        self.assertEqual(parser.occurences()['3'], 1)
        parser = QueryParser(self.query_name_brands)
        self.assertEqual(parser.occurences()['1'], 3)
        self.assertEqual(parser.occurences()['2'], 2)
        self.assertEqual(parser.occurences()['3'], 1)
        parser = QueryParser(self.one_result_query)
        self.assertEqual(parser.occurences()['2'], 1)

    def test_order_found_products(self):
        parser = QueryParser(self.query_name_brands)
        parser.order_found_products()
        self.assertEqual(parser.product_list[0].reference, '1')
        self.assertEqual(parser.product_list[1].reference, '2')
        self.assertEqual(parser.product_list[2].reference, '3')
        parser = QueryParser(self.one_result_query)
        parser.order_found_products()
        self.assertEqual(parser.product_list[0].reference, '2')
