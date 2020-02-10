#!/usr/bin/env python
from django.db.models import Q
from .models import Category, Favorite, Product

class ResultsParser:

    def __init__(self, product):
        self.product = product
