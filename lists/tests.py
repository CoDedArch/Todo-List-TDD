from django.urls import resolve
from django.test import TestCase
from lists.views import home_page
from django.template.loader import render_to_string
from lists.models import Item 

# Create your tests here.
class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page(self) -> None:
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    """
    def test_home_page_returns_correct_html(self) -> None:
        request = HttpRequest() #this is a request object that we manually created to our view
        response = home_page(request) #resolves into a HttpResponse object
        html = response.content.decode('utf-8')
        self.assertTrue(html.startswith('<html>'))
        self.assertin('<title>To-Do</title>', html)
        self.assertTrue(html.endswith('</html>'))

        we can also render our template here
        expected_response = render_to_string('home.html')
        self.assertEqual(html, expected_response)

    """

    def test_home_page_returns_correct_html(self) -> None:
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    
    def test_can_save_a_POST_request(self) -> None:
        response = self.client.post('/', data = {'item_text': 'A new item list'})
        self.assertIn('A new item list', response.content.decode('utf-8'))
        self.assertTemplateUsed(response, 'home.html')


class ItemModelTest(TestCase):
    
    def test_saving_and_retrieving_items(self) -> None:
        first_item = Item()
        first_item.text = 'The First (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual('The First (ever) list item', first_saved_item.text )
        self.assertEqual('Item the second', second_saved_item.text )
