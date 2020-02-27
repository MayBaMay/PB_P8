#!/usr/bin/env python
import unicodedata
from django.db.models import Q
from .models import Category, Favorite, Product

class QueryParser:

    def __init__(self, query):
        self.query = query
        self.product_list = []
        self.query_list = self.split_upper_no_accent(self.query)
        self.order_found_products()

    def split_upper_no_accent(self, sentence):
        query_up = sentence.upper()
        query_up_no_accent = self.no_accent(query_up)
        return query_up_no_accent.split()

    def no_accent(self, sentence):
        sentence_no_accent = ''.join((c for c in unicodedata.normalize('NFD', sentence) if unicodedata.category(c) != 'Mn'))
        return sentence_no_accent

    def products_with_words(self):
    # find all products with one on the word in it
        q_objects = Q()
        for word in self.query_list:
            if word not in ['DE', 'DES', 'LE', 'LA', 'LES', 'AU', 'AUX', 'A']:
                q_objects.add(Q(formated_name__contains=word), Q.OR)
                q_objects.add(Q(formated_brands__contains=word), Q.OR)
        return Product.objects.filter(q_objects).distinct()

    def products_infos(self):
    # for those products, get name and brand in a same list
        product_dict = {}
        for product in self.products_with_words():
            name_brand_string = product.formated_name
            name_brand_string += " "
            name_brand_string += product.formated_brands
            list_name_brand_string = name_brand_string.split()
            product_dict[product.id] = list_name_brand_string
        return product_dict

    def occurences(self):
    # find occurences of words in query and in name_brand_string
    # one occurence by word
        occurences = self.products_infos()
        for key, value in occurences.items():
            found = 0
            for word in self.query_list:
                if word in value:
                    found += 1
            occurences[key] = found
        return occurences

    def order_found_products(self):
        # load products references in an ordered list
        products_ordered = sorted(self.occurences().items(), key=lambda t: t[1], reverse=True)
        for product in products_ordered:
            product = Product.objects.get(id=product[0])
            self.product_list.append(product)
