#!/usr/bin/env python
from django.db.models import Q
from .models import Category, Favorite, Product

class QueryParser:

    def __init__(self, query):
        self.query = query
        self.product_list = []
        self.order_found_products()

    def split_upper(self, sentence):
        query_up = sentence.upper()
        return query_up.split()

    def products_with_words(self):
    # find all products with one on the word in it
        query_list = self.split_upper(self.query)
        q_objects = Q()
        for word in query_list:
            q_objects.add(Q(name__icontains=word), Q.OR)
            q_objects.add(Q(brands__icontains=word), Q.OR)
        return Product.objects.filter(q_objects).distinct()

    def products_infos(self):
    # for those products, get name and brand in the the same string
        product_dict = {}
        for product in self.products_with_words():
            name_brand_string = product.name
            name_brand_string += " "
            name_brand_string += product.brands
            list_name_brand_string = self.split_upper(name_brand_string)
            product_dict[product.reference] = list_name_brand_string
        return product_dict

    def occurences(self):
    # find occurences of words in query and in name_brand_string
        query_list = self.split_upper(self.query)
        products_infos = self.products_infos()
        for key, value in products_infos.items():
            found = 0
            for word in value:
                if word in query_list:
                    found += 1
            products_infos[key] = found
        return products_infos

    def order_found_products(self):
        # load products references in an ordered list
        products_ordered = sorted(self.occurences().items(), key=lambda t: t[1], reverse=True)
        for product in products_ordered:
            self.product_list.append(Product.objects.get(reference=product[0]))
