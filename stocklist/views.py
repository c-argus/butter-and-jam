from django.shortcuts import render, get_object_or_404

# Create your views here.
# Create view to fetch data from the database

from stocklist.models import Item


def home(request):
    # Fetch all items from the database
    items = Item.objects.all()  

    # Set the welcome message
    welcome_message = "Welcome to Cabare's Stocklist homepage!"

    context = {
        'welcome_message': welcome_message,
        'items': items,  # Provide the items queryset to be used in the template
    }
    return render(request, 'home.html', context)


def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})


def item_detail(request, item_id):
    item = Item.objects.get(id=item_id)
    needs_reorder = item.needs_reorder()  # Call the needs_reorder method
    return render(request, 'item_detail.html', {'item': item, 'needs_reorder': needs_reorder})
