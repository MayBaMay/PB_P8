#!/usr/bin/env python
from django.test import TestCase
from ..models import Category, Favorite, Product
from ..results_parser import ResultsParser


class FilterFoundSubstitutesTestCase(TestCase):

    def SetUp(self):
        pass
