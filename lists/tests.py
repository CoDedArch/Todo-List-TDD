from urllib import response
from django.urls import resolve
from django.test import TestCase
from lists.views import home_page, new_list, view_list
from django.template.loader import render_to_string
from lists.models import Item, List 

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
    
    # def test_can_save_a_POST_request(self) -> None:
    #     self.client.post('/', data = {'item_text': 'A new item list'})
    #     self.assertEqual(Item.objects.count(), 1)
    #     new_item = Item.objects.first()
    #     self.assertEqual(new_item.text, 'A new item list')

    # def test_redirects_afeter_a_POST(self) -> None:
    #     response = self.client.post('/', data = {'item_text': 'A new item list'})
    #     self.assertRedirects(response, '/lists/the-only-list-in-the-world/')

class ListViewTest(TestCase):

    def test_url_resolves_to_view_function(self) -> None:
        found = resolve('/lists/the-only-list-in-the-world/')
        self.assertEqual(found.func, view_list)
    def test_uses_list_template(self) -> None:
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_list_items(self) -> None:
        list_ = List.objects.create()
        Item.objects.create(text = 'Itemey 1', list = list_)
        Item.objects.create(text = 'Itemey 2', list = list_)

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'Itemey 1')
        self.assertContains(response, 'Itemey 2')


class NewListItems(TestCase):
    def test_url_resolves_to_fucntion(self) -> None:
        found = resolve('/lists/new')
        self.assertEqual(found.func, new_list)

    def test_can_save_a_POST_request(self) -> None:
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.all()[0]
        self.assertEqual(new_item.text, 'A new list item')

    def test_Redirect_after_a_POST(self) -> None:
        response = self.client.post('/lists/new', data = { 'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')




class ListAndItemModelsTest(TestCase):
    
    def test_saving_and_retrieving_items(self) -> None:
        list_ = List() #the name of the table is the name of the class 
        list_.save()

        first_item = Item()
        first_item.text = 'The First (ever) list item'
        first_item.list = list_ 
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual('The First (ever) list item', first_saved_item.text )
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual('Item the second', second_saved_item.text )
        self.assertEqual(second_saved_item.list, list_)
