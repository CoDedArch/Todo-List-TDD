from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

# Create your views here.

def home_page(request):
    # item = Item()
    # item.text = request.POST.get('item_text', '')
    # item.save()
    if request.method == 'POST':
        Item.objects.create(text = request.POST.get('item_text', ''))
        return redirect('/')
        
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items,})

