#!/usr/bin/env python
from .models import Category, Favorite, Product

class SaveFavorite:

    def __init__(self, current_user, substitute, product_id):
        self.current_user = current_user
        self.substitute = substitute
        self.product_id = product_id
        self.find_favorite()


    def find_favorite(self):
        if Favorite.objects.filter(user=self.current_user, product=self.substitute).exists():
            self.previous = True
            self.update_initial_product()
        else:
            self.previous = False
            self.add_substitute()

    def update_initial_product(self):
        favorite = Favorite.objects.get(user=self.current_user, product=self.substitute)
        favorite.initial_search_product = self.product_id
        favorite.save()

    def add_substitute(self):
        Favorite.objects.create(user=self.current_user, product=self.substitute, initial_search_product=self.product_id)
