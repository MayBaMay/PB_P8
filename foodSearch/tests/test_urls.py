from django.test import SimpleTestCase
from django.urls import resolve, reverse
from ..views import index, legals, register_view, login_view, userpage, watchlist, search, results, detail, load_favorite

class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
        url = reverse('foodSearch:index')
        self.assertEquals(resolve(url).func, index)

    def test_legals_url_is_resolved(self):
        url = reverse('foodSearch:legals')
        self.assertEquals(resolve(url).func, legals)

    def test_register_view_url_is_resolved(self):
        url = reverse('foodSearch:register')
        self.assertEquals(resolve(url).func, register_view)

    def test_login_url_is_resolved(self):
        url = reverse('foodSearch:login')
        self.assertEquals(resolve(url).func, login_view)

    def test_userpage_url_is_resolved(self):
        url = reverse('foodSearch:userpage')
        self.assertEquals(resolve(url).func, userpage)

    def test_watchlist_url_is_resolved(self):
        url = reverse('foodSearch:watchlist')
        self.assertEquals(resolve(url).func, watchlist)

    def test_search_url_is_resolved(self):
        url = reverse('foodSearch:search')
        self.assertEquals(resolve(url).func, search)

    def test_results_url_is_resolved(self):
        url = reverse('foodSearch:results', args=[00000])
        self.assertEquals(resolve(url).func, results)

    def test_detail_url_is_resolved(self):
        url = reverse('foodSearch:detail', args=[00000])
        self.assertEquals(resolve(url).func, detail)

    def test_load_favorite_url_is_resolved(self):
        url = reverse('foodSearch:load_favorite')
        self.assertEquals(resolve(url).func, load_favorite)
