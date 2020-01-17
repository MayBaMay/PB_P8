
""" This module defines the number of datas we want to get from OpenFoodFacts"""


import math

# Products by categories
NB_PRODUCT = 4
PRODUCTS_PER_PAGE = 2
NB_PAGES = math.ceil(NB_PRODUCT/PRODUCTS_PER_PAGE)

# Number of categories
NB_CATEGORIES = 5

# Minimum number of products in a categorie to use it in app
MINPRODINCAT = 10000
