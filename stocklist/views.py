from django.shortcuts import render, redirect, get_object_or_404
from .forms import ItemForm
from stocklist.models import Item

# Create your views here.
# Create view to fetch data from the database


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

def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home page after adding item
    else:
        form = ItemForm()
    return render(request, 'add_item.html', {'form': form})

def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})


def item_detail(request, item_id):
    item = Item.objects.get(id=item_id)
    needs_reorder = item.needs_reorder()  # Call the needs_reorder method
    return render(request, 'item_detail.html', {'item': item, 'needs_reorder': needs_reorder})

def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ItemForm(instance=item)
    return render(request, 'edit_item.html', {'form': form})

def toggle_item_status(request, item_id):
    item = Item.objects.get(pk=item_id)
    item.status = not item.status  # Toggle the status
    item.save()
    return redirect('home')  # Redirect back to the home page

def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect('home')
