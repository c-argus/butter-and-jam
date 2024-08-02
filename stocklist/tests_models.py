# stocklist/tests_models.py

from django.test import TestCase
from django.contrib.auth.models import User
from stocklist.models import Item, Notification

class ItemModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.item = Item.objects.create(
            name="Test Item",
            price=10.00,
            quantity=10,
            reorder_level=5,
            status=True,
            reorder_threshold=5,
            added_by=self.user
        )

    def test_string_representation(self):
        item = Item(name="Sample Item", price=15.00, quantity=20)
        self.assertEqual(str(item), "Sample Item (Price: €15.00, Quantity: 20)")

    def test_needs_reorder(self):
        item = Item(name="Sample Item", price=15.00, quantity=3, reorder_threshold=5)
        self.assertTrue(item.needs_reorder())
        item.quantity = 5
        self.assertFalse(item.needs_reorder())

    def test_item_creation(self):
        self.assertIsInstance(self.item, Item)
        self.assertEqual(self.item.name, "Test Item")
        self.assertEqual(self.item.price, 10.00)
        self.assertEqual(self.item.quantity, 10)
        self.assertEqual(self.item.reorder_level, 5)
        self.assertEqual(self.item.status, True)
        self.assertEqual(self.item.reorder_threshold, 5)
        self.assertEqual(self.item.added_by, self.user)

    def test_notification_creation_on_save(self):
        item = Item.objects.create(
            name="Another Item",
            price=20.00,
            quantity=2,
            reorder_threshold=5,
            added_by=self.user
        )
        item.save()
        notification = Notification.objects.filter(item=item).first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.message, f"The stock for {item.name} has fallen below the reorder threshold of {item.reorder_threshold}.")

class NotificationModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.item = Item.objects.create(
            name="Test Item",
            price=10.00,
            quantity=10,
            reorder_level=5,
            status=True,
            reorder_threshold=5,
            added_by=self.user
        )
        self.notification = Notification.objects.create(
            item=self.item,
            message="Test Notification"
        )

    def test_string_representation(self):
        self.assertEqual(str(self.notification), f"Notification for {self.item.name}: {self.notification.message}")

    def test_notification_creation(self):
        self.assertIsInstance(self.notification, Notification)
        self.assertEqual(self.notification.item, self.item)
        self.assertEqual(self.notification.message, "Test Notification")
        self.assertFalse(self.notification.read)

