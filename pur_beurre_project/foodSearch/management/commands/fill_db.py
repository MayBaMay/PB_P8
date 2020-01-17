#! /usr/bin/env python3
# coding: utf-8

from django.core.management.base import BaseCommand, CommandError
from foodSearch.models import Category, Product, Favorite

from foodSearch.get_datas_from_OFF import GetDatas
from foodSearch.db_init import DbInnit


class Command(BaseCommand):

    def handle(self, *args, **options):
        datas = GetDatas()
        db = DbInnit()
        db.insert_categories(datas.categories_list)
        self.stdout.write(self.style.SUCCESS('Successfully load categories'))
        db.insert_products(datas.products_list)
        self.stdout.write(self.style.SUCCESS('Successfully load products'))
