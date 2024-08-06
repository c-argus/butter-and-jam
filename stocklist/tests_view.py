from django.test import TestCase
from django.urls import reverse
from .models import Item
from django.contrib.auth.models import User


class ViewTests(TestCase):

    def setUp(self):
        """Set up test environment."""
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='testuser', password='12345')
        self.item = Item.objects.create(
            name='Test Item',
            price=10.0,
            quantity=5,
            reorder_threshold=2,
            added_by=self.user
        )

    def test_edit_item_view(self):
        """Test the edit item view."""
        response = self.client.get(reverse('edit_item', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_item.html')

    def test_item_detail_view(self):
        """Test the item detail view."""
        response = self.client.get(reverse('item_detail', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stocklist/item_detail.html')

    def test_item_list_view(self):
        """Test the item list view."""
        response = self.client.get(reverse('item_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stocklist/item_list.html')









