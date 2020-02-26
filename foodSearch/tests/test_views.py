#!/usr/bin/env python
from django.urls import reverse
from django.test import TestCase

from django.contrib.auth.models import User

from ..models import Category, Favorite, Product

class IndexPageTestCase(TestCase):

    # test that index returns a 200
    # must start with `test`
    def test_index_page(self):
        # you must add a name to index view: `name="index"`
        response = self.client.get(reverse('foodSearch:index'))
        self.assertEqual(response.status_code, 200)

# class RegisterPageTestCase(TestCase):
#
#     # ran before each test.
#     def setUp(self):
#         user = User.objects.create(username='UserTest', email='test@test.com', password='test')
#         self.user = User.objects.get(username='UserTest')
#
#     # test that detail page returns a 200 if the item exists
#     def test_register_page_returns_200(self):
#         response = self.client.get(reverse('foodSearch:register'))
#         self.assertEqual(response.status_code, 200)
#
#     # test that a new register is made
#     def test_new_account_is_registered(self):
#         old_accounts = User.objects.count()
#         username = self.user.username
#         password = self.user.password
#         response = self.client.post(reverse('login'), {
#             'username': username,
#             'password': password
#         })
#         new_accounts = User.objects.count()
#         self.assertEqual(new_accounts, old_accounts + 1)
