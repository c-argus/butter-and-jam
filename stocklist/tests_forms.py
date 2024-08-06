# stocklist/tests_forms.py

from django.test import TestCase
from stocklist.forms import ItemForm, UserRegistrationForm
from django.contrib.auth.models import User


class ItemFormTest(TestCase):
    def test_item_form_valid_data(self):
        form = ItemForm(data={
            'name': 'Test Item',
            'price': 10.99,
            'quantity': 5,
        })
        self.assertTrue(form.is_valid())

    def test_item_form_invalid_quantity(self):
        form = ItemForm(data={
            'name': 'Test Item',
            'price': 10.99,
            'quantity': -1,  # Invalid quantity
        })
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)
        self.assertEqual(
            form.errors['quantity'],
            ['Ensure this value is greater than or equal to 0.']
        )

    def test_item_form_fields(self):
        form = ItemForm()
        self.assertEqual(form._meta.fields, ['name', 'price', 'quantity'])


class UserRegistrationFormTest(TestCase):
    def test_user_registration_form_valid_data(self):
        form = UserRegistrationForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
        })
        self.assertTrue(form.is_valid())

    def test_user_registration_form_password_mismatch(self):
        form = UserRegistrationForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password456',  # Passwords do not match
        })
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertEqual(
            form.errors['__all__'],
            ['Passwords do not match']
        )

    def test_user_registration_form_fields(self):
        form = UserRegistrationForm()
        self.assertEqual(
            form._meta.fields, ['username', 'email', 'password']
        )





