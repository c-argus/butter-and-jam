from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User

from .forms import ItemForm, UserRegistrationForm
from .models import Item, Notification


def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(
                request, 'Registration successful. Please log in.'
            )
            return redirect('login')
        else:
            messages.error(
                request, 'There was an error with your registration.'
            )
    else:
        form = UserRegistrationForm()

    return render(request, 'stocklist/register.html', {'form': form})


def custom_login(request):
    """Handle user login."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    else:
        return render(request, 'stocklist/login.html')


@login_required
def home(request):
    """Render the home page."""
    items = Item.objects.all()
    user = request.user
    unread_notifications_count = Notification.objects.filter(
        read=False
    ).count()
    context = {
        'items': items,
        'user': user,
        'unread_notifications_count': unread_notifications_count,
    }
    return render(request, 'home.html', context)


@login_required
def add_item(request):
    """Handle adding a new item."""
    price_error = None

    if request.method == 'POST':
        item_form = ItemForm(request.POST, prefix='item')
        if item_form.is_valid():
            item_price = request.POST.get('item-price')
            try:
                item_price = float(item_price)
                if item_price < 0:
                    price_error = "Price cannot be negative."
            except ValueError:
                price_error = "Invalid price format."

            if not price_error:
                item = item_form.save(commit=False)
                item.added_by = request.user
                item.save()
                if item.quantity < item.reorder_threshold:
                    Notification.objects.filter(item=item).delete()
                    Notification.objects.create(
                        item=item,
                        message=(
                            f"The stock for {item.name} is now below "
                            "the reorder point."
                        ),
                    )
                messages.success(request, 'Item added with success')
                return redirect('add_item')
        else:
            messages.error(request, 'There was an error adding the item')
    else:
        item_form = ItemForm(prefix='item')

    return render(
        request, 'add_item.html', {
            'item_form': item_form, 'price_error': price_error
        }
    )


@login_required
def item_list(request):
    """Render the list of items."""
    items = Item.objects.all()
    return render(request, 'stocklist/item_list.html', {'items': items})


def item_detail(request, item_id):
    """Render the detail view of an item."""
    item = get_object_or_404(Item, id=item_id)
    needs_reorder = item.needs_reorder()
    return render(
        request, 'stocklist/item_detail.html', {
            'item': item, 'needs_reorder': needs_reorder
        }
    )


@login_required
def edit_item(request, item_id):
    """Handle editing an existing item."""
    user = request.user
    if not user.is_staff:
        return redirect('home')
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        item_form = ItemForm(request.POST, instance=item, prefix='item')
        if item_form.is_valid():
            item = item_form.save()
            if item.quantity < item.reorder_threshold:
                Notification.objects.filter(item=item).delete()
                Notification.objects.create(
                    item=item,
                    message=(
                        f"The stock for {item.name} has fallen below "
                        "the reorder threshold."
                    ),
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
    """Handle deleting an item."""
    user = request.user
    if not user.is_staff:
        return redirect('home')
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    messages.success(request, 'Item deleted successfully')
    return redirect('home')


@login_required
def notifications(request):
    """Render the notifications page."""
    user = request.user
    if not user.is_staff:
        return redirect('home')
    notifications = Notification.objects.all()
    return render(
        request, 'stocklist/notifications.html', {
            'notifications': notifications
        }
    )


@require_POST
@login_required
@csrf_exempt
def mark_notification_as_read(request, notification_id):
    """Mark a notification as read."""
    notification = get_object_or_404(Notification, id=notification_id)
    notification.read = True
    notification.save()
    data = {
        'message': 'Notification marked as read',
    }
    return JsonResponse(data)



