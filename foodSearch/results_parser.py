#!/usr/bin/env python
import time
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from .models import Category, Favorite, Product

def fctSortDict(value):
    return value['nb']

class ResultsParser:

    def __init__(self, product_id, current_user):
        start_time = time.time()
        self.product = Product.objects.get(id=product_id)
        self.current_user = current_user
        self.all_results = self.products_same_categories()
        self.relevant_results_queryset = self.get_results_queryset()
        self.results_infos = self.get_results_dict_with_favorite_info()

        if self.relevant_results_queryset.count() > 6:
            self.paginate = True
        else:
            self.paginate = False
        print(round((time.time() - start_time),1))

    def products_same_categories(self):
        results=[]
        loaded_products_ids = []
        # found categories linked to this product
        found_categories = Category.objects.filter(products__id=self.product.id)
        nb_found_categories = found_categories.count()

        # get 3 most specifics categories of the product (last 3)
        if nb_found_categories > 3:
            specific_categories = found_categories[nb_found_categories-3: nb_found_categories]
        else:
            specific_categories = found_categories

        if self.product.nutrition_grade_fr == 'a':
            #for each category of the product asked
            for category in specific_categories:
                # for product in this category
                for compared_prod in Product.objects.filter(categories__reference=category.reference):
                    if compared_prod.nutrition_grade_fr == self.product.nutrition_grade_fr:
                        self.compare_products_categories(results, loaded_products_ids, compared_prod, found_categories)
        else:
            #for each category of the product asked
            for category in specific_categories:
                # for product in this category
                for compared_prod in Product.objects.filter(categories__reference=category.reference):
                    if compared_prod.nutrition_grade_fr < self.product.nutrition_grade_fr:
                        self.compare_products_categories(results, loaded_products_ids, compared_prod, found_categories)
        return results

    def compare_products_categories(self, results, loaded_products_ids, compared_prod, found_categories):
        # avoid duplication
        if compared_prod.id not in loaded_products_ids:
            # get common categories for each product and occurences with the searched product
            count_same_categories = 0 #count nb of categories in common
            common_categories = [] #id of those categories
            for compared_category in Category.objects.filter(products__id=compared_prod.id):
                if compared_category in found_categories:
                    if compared_category.id not in common_categories:
                        common_categories.append(compared_category.id)
                        count_same_categories += 1
            # save product as already treated, avoid duplications
            loaded_products_ids.append(compared_prod.id)
            # get informations in dictionnary contained in the list results
            results.append({'id':compared_prod.id, 'nb':count_same_categories})

    def get_most_relevant_products(self):
        # get the 24 firsts most relevant products in an ordered queryset
        results = sorted(self.all_results, key=fctSortDict, reverse=True)
        results24 = results[0:24]
        return results24

    def get_results_queryset(self):
        q_objects = Q()
        for item in self.get_most_relevant_products():
            q_objects.add(Q(id=item['id']), Q.OR)
        result_QuerySet = Product.objects.filter(q_objects).order_by('nutrition_grade_fr')
        return result_QuerySet

    def get_results_dict_with_favorite_info(self):
        # result in dictionnary with key=object & value=boolean(product already in favorite)
        results_infos = []
        for result in self.relevant_results_queryset:
            if self.current_user.is_authenticated:
                if Favorite.objects.filter(substitute=result, user=self.current_user).exists():
                    results_infos.append({result: True})
                else:
                    results_infos.append({result: False})
            else:
                results_infos.append({result: False})
        return results_infos

    def paginator(self, page):
        if self.paginate:
            paginator = Paginator(self.results_infos, 6)
            page_results = paginator.get_page(page)
        else:
            page_results = self.results_infos
        return page_results
