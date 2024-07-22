from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ItemForm
from .models import Item, Notification
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Custom login view
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'stocklist/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'stocklist/login.html')

@login_required
def home(request):
    items = Item.objects.all()
    welcome_message = "Welcome to Cabare's Stocklist homepage!"
    context = {
        'welcome_message': welcome_message,
        'items': items,
    }
    return render(request, 'home.html', context)

@login_required
def add_item(request):
    if request.method == 'POST':
        item_form = ItemForm(request.POST, prefix='item')
        if item_form.is_valid():
            item = item_form.save()
            if item.quantity < item.reorder_threshold:
                Notification.objects.create(
                    item=item,
                    message=f"The stock for {item.name} has fallen below the reorder threshold."
                )
            messages.success(request, 'Item added successfully')
            return redirect('home')
        else:
            messages.error(request, 'There was an error adding the item')
    else:
        item_form = ItemForm(prefix='item')
    return render(request, 'add_item.html', {'item_form': item_form})

def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    needs_reorder = item.needs_reorder()
    return render(request, 'item_detail.html', {'item': item, 'needs_reorder': needs_reorder})

@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        item_form = ItemForm(request.POST, instance=item, prefix='item')
        if item_form.is_valid():
            item = item_form.save()
            if item.quantity < item.reorder_threshold:
                Notification.objects.filter(item=item).delete()
                Notification.objects.create(
                    item=item,
                    message=f"The stock for {item.name} has fallen below the reorder threshold."
                )
            
            messages.success(request, 'Item updated successfully')
            return redirect('home')
        else:
            messages.error(request, 'There was an error updating the item')
    else:
        item_form = ItemForm(instance=item, prefix='item')
    return render(request, 'edit_item.html', {'item_form': item_form})

@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    messages.success(request, 'Item deleted successfully')
    return redirect('home')

@login_required
def notifications(request):
    notifications = Notification.objects.all()
    return render(request, 'stocklist/notifications.html', {'notifications': notifications})

@require_POST
@login_required
@csrf_exempt
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.read = True
    notification.save()
    data = {
        'message': 'item updated successfully',
    }
    return JsonResponse(data)


