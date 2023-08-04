from django.shortcuts import render,get_object_or_404

# Create your views here.
# Create view to fetch data from the database

from stocklist.models import Item

def home(request):
    
    context = {
        'message': 'Welcome to the homepage!',
    }
    return render(request, 'home.html', context)


def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})


def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'item_detail.html', {'item': item})
