#!/usr/bin/env python
from .models import Category, Favorite, Product

class SaveFavorite:

    def __init__(self, current_user, substitute, product):
        self.current_user = current_user
        self.substitute = substitute
        self.product = product

    def previous(self):
        if Favorite.objects.filter(user=self.current_user, substitute=self.substitute).exists():
            self.previous = True
        else:
            self.previous = False

    def find_favorite(self):
        if self.previous = True
            self.update_initial_product()
        else:
            self.add_substitute()

    def update_initial_product(self):
        favorite = Favorite.objects.get(user=self.current_user, substitute=self.substitute)
        favorite.initial_search_product = self.product
        favorite.save()

    def add_substitute(self):
        Favorite.objects.create(user=self.current_user, substitute=self.substitute, initial_search_product=self.product)
