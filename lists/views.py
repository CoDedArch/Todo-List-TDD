from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from lists.models import Item, List

# Create your views here.

def home_page(request):
    return render(request, 'home.html')

def view_list(request, list_id):
    list_ = List.objects.get(id = list_id)
    return render(request, 'list.html', {'list': list_})

def new_list(request):
    """/lists/new is the url that resovles to this function. this is a non trailing / which means 
    it changes the state of our database
    """
    list_ = List.objects.create()
    Item.objects.create(text= request.POST.get('item_text', ''), list = list_)
    return redirect(f'/lists/{list_.id}/')
    
def add_item(request,list_id):
    list_ = List.objects.get(id= list_id)
    Item.objects.create(text= request.POST.get('item_text', ''), list = list_)
    return redirect(f'/lists/{list_.id}/')