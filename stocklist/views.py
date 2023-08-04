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
    item = Item.objects.get(id=item_id)
    needs_reorder = item.needs_reorder()  # Call the needs_reorder method
    return render(request, 'item_detail.html', {'item': item, 'needs_reorder': needs_reorder})
