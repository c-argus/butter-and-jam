# Import necessary modules
from django import forms
from .models import Item

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




    

