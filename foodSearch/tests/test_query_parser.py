#!/usr/bin/env python
from django.test import TestCase
from ..models import Category, Favorite, Product
from ..query_parser import QueryParser

class FilterFoundProductsTestCase(TestCase):

    def setUp(self):
        Product.objects.create(id=31, name="Fàke product for db", formated_name="FAKE PRODUCT FOR DB", brands="brand fake", formated_brands="BRAND FAKE", reference='1')
        Product.objects.create(id=32, name="Second fake prôduct", formated_name="SECOND FAKE PRODUCT", brands="the wrong one", formated_brands="THE WRONG ONE", reference='2')
        Product.objects.create(id=33, name="product", formated_name="PRODUCT", brands="not bad", formated_brands="NOT BAD", reference='3')
        self.exact_query = "product"
        self.query_name = "fàke product"
        self.query_name_brands = "fake prôduct brand"
        self.one_result_query = "Sécond"

    def test_upper_no_accent(self):
        parser = QueryParser(self.query_name_brands)
        self.assertEqual(parser.upper_no_accent(self.query_name_brands), 'FAKE PRODUCT BRAND')
        parser = QueryParser(self.one_result_query)
        self.assertEqual(parser.upper_no_accent(self.one_result_query), 'SECOND')

    def test_get_exact_query_list(self):
        parser = QueryParser(self.query_name_brands)
        self.assertEqual(parser.get_exact_query_list(), False)
        parser = QueryParser(self.exact_query)
        self.assertEqual(parser.get_exact_query_list().count(), 1)

    def test_get_query_list(self):
        parser = QueryParser(self.exact_query)
        self.assertEqual(len(parser.product_list), 4)
        self.assertEqual(parser.product_list[0].id, 33)
        parser = QueryParser(self.query_name)
        self.assertEqual(parser.product_list[0].id, 31)
        parser = QueryParser(self.query_name_brands)
        self.assertEqual(parser.product_list[0].id, 31)
        parser = QueryParser(self.one_result_query)
        self.assertEqual(parser.product_list[0].id, 32)


    def test_products_with_words(self):
        parser = QueryParser(self.query_name)
        self.assertEqual(parser.products_with_words().count(), 3)
        parser = QueryParser(self.query_name_brands)
        self.assertEqual(parser.products_with_words().count(), 3)
        parser = QueryParser(self.one_result_query)
        self.assertEqual(parser.products_with_words().count(), 1)

    def test_products_infos(self):
        parser = QueryParser(self.query_name)
        self.assertEqual(parser.products_infos()[31], ["FAKE", "PRODUCT", "FOR", "DB", "BRAND", "FAKE"])
        self.assertEqual(parser.products_infos()[32], ["SECOND", "FAKE", "PRODUCT", "THE", "WRONG", "ONE"])
        self.assertEqual(parser.products_infos()[33], ["PRODUCT", "NOT", "BAD"])
        parser = QueryParser(self.query_name_brands)
        self.assertEqual(parser.products_infos()[31], ["FAKE", "PRODUCT", "FOR", "DB", "BRAND", "FAKE"])
        self.assertEqual(parser.products_infos()[32], ["SECOND", "FAKE", "PRODUCT", "THE", "WRONG", "ONE"])
        self.assertEqual(parser.products_infos()[33], ["PRODUCT", "NOT", "BAD"])
        parser = QueryParser(self.one_result_query)
        self.assertEqual(parser.products_infos()[32], ["SECOND", "FAKE", "PRODUCT", "THE", "WRONG", "ONE"])

    def test_occurences(self):
        parser = QueryParser(self.query_name)
        self.assertEqual(parser.occurences()[31], 2)
        self.assertEqual(parser.occurences()[32], 2)
        self.assertEqual(parser.occurences()[33], 1)
        parser = QueryParser(self.query_name_brands)
        self.assertEqual(parser.occurences()[31], 3)
        self.assertEqual(parser.occurences()[32], 2)
        self.assertEqual(parser.occurences()[33], 1)
        parser = QueryParser(self.one_result_query)
        self.assertEqual(parser.occurences()[32], 1)

    def test_order_found_products(self):
        parser = QueryParser(self.query_name_brands)
        self.assertEqual(parser.order_found_products()[0], (31, 3))
        self.assertEqual(parser.order_found_products()[1], (32, 2))
        self.assertEqual(parser.order_found_products()[2], (33, 1))
        parser = QueryParser(self.one_result_query)
        self.assertEqual(parser.order_found_products()[0], (32, 1))
