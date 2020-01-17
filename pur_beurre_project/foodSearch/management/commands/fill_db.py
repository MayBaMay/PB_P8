#! /usr/bin/env python3
# coding: utf-8

"""
This module manage insertion database.
"""
from django.core.management.base import BaseCommand, CommandError
from foodSearch.models import Category, Product, Favorite
from _get_datas_form_OFF import GetDatas
from _db_fill import DbFill

class Command(BaseCommand):
    """
    Insert data in PostGreSQL database.
    """

    pass
