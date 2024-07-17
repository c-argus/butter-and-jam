from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required  # Import decorator for login requirement
from django.contrib import messages  # Import messages framework for user feedback
from .forms import ItemForm
from .models import Item
from django.contrib.auth import authenticate, login

# Create your views here.
# Create view to fetch data from the database

# Custom login view
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home or another page after login
        else:
            # Handle invalid login
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

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

# View for adding a new item.
@login_required  # Ensure user is logged in to access this view
def add_item(request):
    if request.method == 'POST':
        item_form = ItemForm(request.POST, prefix='item')
                
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.reorder_threshold = 5  # Set default reorder threshold value
            item.save()
            messages.success(request, 'Item added successfully')  # Success message
            return redirect('home')  # Redirect to home page after adding item
        else:
            messages.error(request, 'There was an error adding the item')  # Error message if form is not valid
    else:
        item_form = ItemForm(prefix='item')
    
    return render(request, 'add_item.html', {'item_form': item_form})

# View for displaying a list of items
def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})

# View for details of a specific item, including whether it needs to be reordered.
def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    needs_reorder = item.needs_reorder()
    return render(request, 'item_detail.html', {'item': item, 'needs_reorder': needs_reorder})

# View for editing an existing item
@login_required  # Ensure user is logged in to access this view
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    threshold_instance = item.threshold if hasattr(item, 'threshold') else None

    if request.method == 'POST':
        item_form = ItemForm(request.POST, instance=item, prefix='item')
        if item_form.is_valid():  
            item_form.save()
            messages.success(request, 'Item updated successfully')  # Success message
            return redirect('home')
        else:
            messages.error(request, 'There was an error updating the item')  # Error message if form is not valid
    else:
        item_form = ItemForm(instance=item, prefix='item')
    return render(request, 'edit_item.html', {'item_form': item_form})

# View for deleting an existing item
@login_required  # Ensure user is logged in to access this view
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)  # Get item by item_id or show 404 page if not found
    item.delete()  # Delete the item from the database
    messages.success(request, 'Item deleted successfully')  # Success message
    return redirect('home')  # Redirect to home page after deleting item
