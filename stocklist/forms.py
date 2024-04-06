# Import necessary modules
from django import forms
from .models import Item

# Define a form class for adding items
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item # Specify the model to use for the form        
        fields = ['name', 'price', 'quantity'] # Specify the fields to include in the form
