from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required  # Import decorator for login requirement
from django.contrib import messages  # Import messages framework for user feedback
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

# View for adding a new item
@login_required  # Ensure user is logged in to access this view
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item added successfully')  # Success message
            return redirect('home')  # Redirect to home page after adding item
        else:
            messages.error(request, 'There was an error adding the item')  # Error message if form is not valid
    else:
        form = ItemForm()
    return render(request, 'add_item.html', {'form': form})

# View for displaying a list of items
def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})

# View for displaying details of a specific item
def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)  # Get item by item_id or show 404 page if not found
    needs_reorder = item.needs_reorder()  # Check if item needs to be reordered
    return render(request, 'item_detail.html', {'item': item, 'needs_reorder': needs_reorder})  # Render item_detail.html template with item and needs_reorder

# View for editing an existing item
@login_required  # Ensure user is logged in to access this view
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully')  # Success message
            return redirect('home')
        else:
            messages.error(request, 'There was an error updating the item')  # Error message if form is not valid
    else:
        form = ItemForm(instance=item)
    return render(request, 'edit_item.html', {'form': form})

# View for deleting an existing item
@login_required  # Ensure user is logged in to access this view
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)  # Get item by item_id or show 404 page if not found
    item.delete()  # Delete the item from the database
    messages.success(request, 'Item deleted successfully')  # Success message
    return redirect('home')  # Redirect to home page after deleting item
