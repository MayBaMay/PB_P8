#!/usr/bin/env python
import json
from django.test import TestCase, Client
from django.urls import reverse
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from  django.contrib.auth.models import User

from ..models import Category, Favorite, Product


class GeneralPagesTestCase(TestCase):

    def test_index_page(self):
        # you must add a name to index view: `name="index"`
        response = self.client.get(reverse('foodSearch:index'))
        self.assertEqual(response.status_code, 200)

    def test_legals_GET(self):
        response = self.client.get(reverse('foodSearch:legals'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foodSearch/legals.html')


class RegisterPageTestCase(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_register(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.selenium.find_element_by_css_selector("#connect").click()
        signin_modal = self.selenium.find_element_by_css_selector("#modalLogIn")
        self.assertTrue(signin_modal.is_displayed())
        self.selenium.find_element_by_css_selector("#registration").click()
        signup_modal = self.selenium.find_element_by_css_selector("#modalRegister")
        self.assertTrue(signup_modal.is_displayed())

        username_input = self.selenium.find_element_by_css_selector("#signUp-username")
        username_input.send_keys('usertest')
        email_input = self.selenium.find_element_by_css_selector("#signUp-email")
        email_input.send_keys('usertest@test.com')
        password_input = self.selenium.find_element_by_css_selector("#signUp-password")
        password_input.send_keys('secret')
        self.selenium.find_element_by_css_selector("#signUp-btn").click()

        self.assertEqual(User.objects.filter(username="usertest").exists(), True)
        self.assertEqual(User.objects.filter(username="usertest").count(), 1)
        self.assertEqual(User.objects.get(username="usertest").is_authenticated, True)

    def test_login(self):
        User.objects.create(username="Test",
                            email="userinDB@test.com",
                            password="password")
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.selenium.find_element_by_css_selector("#connect").click()
        signin_modal = self.selenium.find_element_by_css_selector("#modalLogIn")
        self.assertTrue(signin_modal.is_displayed())
        username_input = self.selenium.find_element_by_css_selector("#login-username")
        username_input.send_keys('Test')
        password_input = self.selenium.find_element_by_css_selector("#login-password")
        password_input.send_keys('password')
        self.selenium.find_element_by_css_selector("#signin-Submit").click()

        self.assertEqual(User.objects.filter(username="Test").exists(), True)
        self.assertEqual(User.objects.filter(username="Test").count(), 1)
        self.assertEqual(User.objects.get(username="Test").is_authenticated, True)

        #
        # self.selenium.find_element_by_css_selector("#disconnection").click()
        # signin_modal = self.selenium.find_element_by_css_selector("#modalLogOut")
        # self.assertTrue(signin_modal.is_displayed())
        # self.selenium.find_element_by_css_selector("#logoutbtn").click()
        # self.assertEqual(User.objects.get(username="Test").is_authenticated, False)


class ProceedResearchTestCase(TestCase):

    def setUp(self):
        self.query = "Product"
        self.prod = Product.objects.create(id=31,
                               name="Fàke product for db",
                               formatted_name="FAKE PRODUCT FOR DB",
                               brands="brand fake",
                               formatted_brands="BRAND FAKE",
                               reference='1')

    def test_search_GET(self):
        response = self.client.get(reverse('foodSearch:search'), {'query': self.query})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foodSearch/search.html')

    def test_result_GET(self):
        response = self.client.get(reverse('foodSearch:results', args=[self.prod.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foodSearch/results.html')

    def test_detail_GET(self):
        response= self.client.get(reverse('foodSearch:detail', args=[self.prod.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'foodSearch/detail.html')


class ManageFavoriteTestCase(StaticLiveServerTestCase):

    def test_watchlist(self):
        pass
        # favorite = Favorite.objects.create(user, substitute, self.prod)
        #login usertest

    def test_load_favorite(self):
        pass
