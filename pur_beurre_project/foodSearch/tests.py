from djanco.core.urlresolvers import reverse
from django.test import TestCase

# Create your tests here.
class IndexPageTestCase(TestCase):
    def test_index_page(self):
        """test that index page url returns a 200 status code"""
        response = self.client.get(reverse('index'))
        self.assertEquel(response.status_code, 200)
        
