from cgitb import text
from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List

# Create your views here.

def home_page(request):
    return render(request, 'home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

def new_list(request):
    """/lists/new is the url that resovles to this function. this is a non trailing / which means 
    it changes the state of our database
    """
    list_ = List.objects.create()
    Item.objects.create(text= request.POST.get('item_text', ''), list = list_)
    return redirect('/lists/the-only-list-in-the-world/')
    
