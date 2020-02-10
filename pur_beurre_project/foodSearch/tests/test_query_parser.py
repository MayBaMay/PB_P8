# #!/usr/bin/env python
# from django.test import TestCase
# from ..models import Category, Favorite, Product
# from ..query_parser import QueryParser
#
# class FilterFoundProductsTestCase(TestCase):
#
#     def setUp(self):
#         Product.objects.create(name="Fake product for db", brands="brand fake", reference="1")
#         Product.objects.create(name="Second fake product", brands="the wrong one", reference="2")
#         Product.objects.create(name="product", brands="not bad", reference="3")
#         self.query_name = "fake product"
#         self.query_name_brands = "fake product brand"
#         self.one_result_query = "Second"
#
#     def test_split_upper(self):
#         self.parser = QueryParser(self.query_name_brands)
#         self.assertEqual(self.parser.split_upper(self.query_name_brands), ['FAKE', 'PRODUCT', 'BRAND'])
#         self.parser = QueryParser(self.one_result_query)
#         self.assertEqual(self.parser.split_upper(self.one_result_query), ['SECOND'])
#
#     def test_products_with_words(self):
#         self.parser = QueryParser(self.query_name)
#         self.assertEqual(self.parser.products_with_words().count(), 3)
#         self.parser = QueryParser(self.query_name_brands)
#         self.assertEqual(self.parser.products_with_words().count(), 3)
#         self.parser = QueryParser(self.one_result_query)
#         self.assertEqual(self.parser.products_with_words().count(), 1)
#
#     def test_products_infos(self):
#         self.parser = QueryParser(self.query_name)
#         self.assertEqual(self.parser.products_infos()['1'], ["FAKE", "PRODUCT", "FOR", "DB", "BRAND", "FAKE"])
#         self.assertEqual(self.parser.products_infos()['2'], ["SECOND", "FAKE", "PRODUCT", "THE", "WRONG", "ONE"])
#         self.assertEqual(self.parser.products_infos()['3'], ["PRODUCT", "NOT", "BAD"])
#         self.parser = QueryParser(self.query_name_brands)
#         self.assertEqual(self.parser.products_infos()['1'], ["FAKE", "PRODUCT", "FOR", "DB", "BRAND", "FAKE"])
#         self.assertEqual(self.parser.products_infos()['2'], ["SECOND", "FAKE", "PRODUCT", "THE", "WRONG", "ONE"])
#         self.assertEqual(self.parser.products_infos()['3'], ["PRODUCT", "NOT", "BAD"])
#         self.parser = QueryParser(self.one_result_query)
#         self.assertEqual(self.parser.products_infos()['2'], ["SECOND", "FAKE", "PRODUCT", "THE", "WRONG", "ONE"])
#
#     def test_occurences(self):
#         self.parser = QueryParser(self.query_name)
#         self.assertEqual(self.parser.occurences()['1'], 3)
#         self.assertEqual(self.parser.occurences()['2'], 2)
#         self.assertEqual(self.parser.occurences()['3'], 1)
#         self.parser = QueryParser(self.query_name_brands)
#         self.assertEqual(self.parser.occurences()['1'], 4)
#         self.assertEqual(self.parser.occurences()['2'], 2)
#         self.assertEqual(self.parser.occurences()['3'], 1)
#         self.parser = QueryParser(self.one_result_query)
#         self.assertEqual(self.parser.occurences()['2'], 1)
#
#     def test_order_found_products(self):
#         self.parser = QueryParser(self.query_name_brands)
#         self.parser.order_found_products()
#         self.assertEqual(self.parser.product_list[0].reference, '1')
#         self.assertEqual(self.parser.product_list[1].reference, '2')
#         self.assertEqual(self.parser.product_list[2].reference, '3')
#         self.parser = QueryParser(self.one_result_query)
#         self.parser.order_found_products()
#         self.assertEqual(self.parser.product_list[0].reference, '2')
