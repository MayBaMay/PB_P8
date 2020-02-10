from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Category, Favorite, Product
from ..favorite import SaveFavorite


class FilterFoundProductsTestCase(TestCase):

    def setUp(self):
        self.current_user = User.objects.create()
        self.prod1 = Product.objects.create(id=1, name="Fake product for db", brands="brand fake", reference="1")
        self.prod2 = Product.objects.create(id=2, name="Second fake product", brands="the wrong one", reference="2")
        self.prod3 = Product.objects.create(id=3, name="product", brands="not bad", reference="3")
        Favorite.objects.create(user=self.current_user, product=self.prod2, initial_search_product=3)

    # check if already in Favorite
    def test_favorite_exists(self):
        self.assertEqual(SaveFavorite(self.current_user, self.prod1, 2).previous, False)
        self.assertEqual(SaveFavorite(self.current_user, self.prod2, 3).previous, True)

    # if yes change initial_product_id if necessary
    def test_update_initial_product(self):
        # pass
        SaveFavorite(self.current_user, self.prod2, 1)
        favorite = Favorite.objects.get(user=self.current_user, product=self.prod2)
        self.assertEqual(favorite.initial_search_product, 1)

    # if not create Favorite
    def test_add_substitute(self):
        SaveFavorite(self.current_user, self.prod1, 3)
        favorite = Favorite.objects.get(user=self.current_user, product=self.prod1)
        self.assertEqual(favorite.initial_search_product, 3)
