from django.test import TestCase
from django.db import IntegrityError
from  django.contrib.auth.models import User
from ..models import Category, Product, Favorite


class TestModels(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="usertest",
                                        email="user@test.com",
                                        password="password")
        self.product1 = Product.objects.create(name="Fàke product for db",
                                               formatted_name="FAKE PRODUCT FOR DB",
                                               brands="good4U",
                                               formatted_brands="GOOD4U",
                                               reference='fakeref1')
        self.product2 = Product.objects.create(name="Second fake prôduct",
                                               formatted_name="SECOND FAKE PRODUCT",
                                               brands="bad4U",
                                               formatted_brands="BAD4U",
                                               reference='fakeref2')
        self.Category1 = Category.objects.create(reference="en:fake-category-for-tests")
        self.Category1.products.add(self.product1)
        self.favorite = Favorite.objects.create(user=self.user,
                                                substitute=self.product1,
                                                initial_search_product=self.product2)

    def test_user_model(self):
        self.assertEqual(User.objects.filter(username="usertest").exists(), True)
        self.assertEqual(User.objects.get(username="usertest").password, 'password')

    def test_product_model(self):
        self.assertEqual(Product.objects.filter(name="Fàke product for db").exists(), True)
        self.assertEqual(Product.objects.get(name="Fàke product for db").brands, 'good4U')

    def test_category_model(self):
        self.assertEqual(Category.objects.filter(reference="en:fake-category-for-tests").exists(), True)
        cat = Category.objects.filter(products__id=self.product1.id)
        self.assertEqual(self.Category1 in cat, True)
        prod = Product.objects.filter(categories__reference=self.Category1.reference)
        self.assertEqual(self.product1 in prod, True)
        self.assertEqual(self.product2 in prod, False)

    def test_favorite_model(self):
        self.assertEqual(self.favorite.user, self.user)
        fav = Favorite.objects.get(substitute=self.product1)
        self.assertEqual(fav.initial_search_product, self.product2)
        # test favorite Meta class unique_together = ('user', 'substitute',)
        with self.assertRaises(Exception) as raised:
            self.favorite = Favorite.objects.create(user=self.user,
                                                    substitute=self.product1,
                                                    initial_search_product=self.product2)
        self.assertEqual(IntegrityError, type(raised.exception))
