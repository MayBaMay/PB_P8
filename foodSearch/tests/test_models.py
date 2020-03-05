from django.test import TestCase
from ..models import Category, Product, Favorite, User

class TestModels(TestCase):

    def setUp(self):
        self.product1 = Product.objects.create(
                name="Fàke product for db",
                formatted_name="FAKE PRODUCT FOR DB",
                brands="brand fake",
                formatted_brands="BRAND FAKE",
                reference='1'
        )
        self.Category1 = Category.objects.create(reference="en:biscuits-and-cakes")
