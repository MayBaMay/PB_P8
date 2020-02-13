#!/usr/bin/env python
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Category, Favorite, Product

def fctSortDict(value):
    return value['nb']

class ResultsParser:

    def __init__(self, product_id):
        self.product = Product.objects.get(id=product_id)
        self.all_results = self.products_same_categories()
        self.relevant_results_queryset = self.get_results_queryset()
        self.results_infos = self.get_results_dict_with_favorite_info()

        if self.relevant_results_queryset.count() != 0:
            self.paginate = True
        else:
            self.paginate = False

    def products_same_categories(self):
        results=[]
        loaded_products_ids = []
        # found categories linked to this product
        found_categories = Category.objects.filter(products__id=self.product.id)
        #for each category of the product asked
        for category in found_categories:
            # for product in this category
            for prod in Product.objects.filter(categories__reference=category.reference):
                # avoid duplication
                if prod.id in loaded_products_ids:
                    pass
                else:
                    if prod.nutrition_grade_fr < self.product.nutrition_grade_fr:
                        # get common categories for each product and occurences with the searched product
                        count_same_categories = 0 #count nb of categories in common
                        common_categories = [] #name of those categories
                        for category in Category.objects.filter(products__id=prod.id):
                            if category in found_categories:
                                if category not in common_categories:
                                    common_categories.append(category)
                                    count_same_categories += 1
                        # get informations in dictionnary contained in the list results
                        results.append({'id':prod.id, 'nb':count_same_categories, 'cats_list':common_categories})
                        loaded_products_ids.append(prod.id)
        return results

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
            if Favorite.objects.filter(substitute=result).exists():
                results_infos.append({result: True})
            else:
                results_infos.append({result: False})
        return results_infos

    def paginator(self, page):
        result = Product.objects.all()
        if self.paginate:
            paginator = Paginator(self.results_infos, 6)
            page_results = paginator.get_page(page)
            return page_results
