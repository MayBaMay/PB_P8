#!/usr/bin/env python
import unicodedata
from django.db.models import Q
from .models import Category, Favorite, Product

class QueryParser:

    def __init__(self, query):
        self.query = query
        self.product_list = []
        self.formatted_query = self.upper_no_accent(self.query)


    def upper_no_accent(self, sentence):
        query_up = sentence.upper()
        query_up_no_accent = self.no_accent(query_up)
        return query_up_no_accent

    def no_accent(self, sentence):
        sentence_no_accent = ''.join((c for c in unicodedata.normalize('NFD', sentence) if unicodedata.category(c) != 'Mn'))
        return sentence_no_accent

    def get_final_list(self):
        i=0
        if self.get_exact_query_set():
            for product in self.get_exact_query_set():
                self.product_list.append(product)
        while len(self.product_list) < 12:
            try:
                self.get_large_list(i)
                i+=1
            except:
                break

    def get_exact_query_set(self):
        products = Product.objects.filter(formated_name=self.formatted_query)
        if products.exists():
            return products
        else:
            return False

    def get_large_list(self, i):
        self.query_list = self.formatted_query.split()
        product = Product.objects.get(id=self.order_found_products()[i][0])
        if product not in self.product_list:
            self.product_list.append(product)

    def products_with_words(self):
    # find all products with one on the word in it
        q_objects = Q()
        for word in self.formatted_query.split():
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
            for word in self.formatted_query.split():
                if word in value:
                    found += 1
            occurences[key] = found
        return occurences

    def order_found_products(self):
        # load products references in an ordered list
        return sorted(self.occurences().items(), key=lambda t: t[1], reverse=True)
