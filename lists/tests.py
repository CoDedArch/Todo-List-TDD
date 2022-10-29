from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest, HttpResponse

from lists.views import home_page 

# Create your tests here.
class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page(self) -> None:
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self) -> None:
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-DO list</title>', html)
        self.assertTrue(html.endswith('</html>'))
