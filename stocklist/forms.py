# Import necessary modules
from django import forms
from .models import Item
from django.contrib.auth.models import User

# Define a form class for adding items
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item # Specify the model to use for the form        
        fields = ['name', 'price', 'quantity'] # Specify the fields to include in the form

    def clean_quantity(self):
        # Custom cleaning method for the quantity field
        quantity = self.cleaned_data.get('quantity')

        # Check if quantity is negative
        if quantity < 0:
            raise forms.ValidationError('Quantity cannot be negative')

        return quantity

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')



    

