# Import necessary modules
from django import forms
from .models import Item, Threshold

# Define a form class for adding items
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item # Specify the model to use for the form        
        fields = ['name', 'price', 'quantity', 'reorder_level'] # Specify the fields to include in the form

    def clean_quantity(self):
        # Custom cleaning method for the quantity field
        quantity = self.cleaned_data.get('quantity')

        # Check if quantity is negative
        if quantity < 0:
            raise forms.ValidationError('Quantity cannot be negative')

        return quantity

    def clean_reorder_level(self):
        # Custom cleaning method for the reorder_level field
        reorder_level = self.cleaned_data.get('reorder_level')

        # Check if reorder_level is negative
        if reorder_level < 0:
            raise forms.ValidationError('Reorder level cannot be negative')
        
        return reorder_level

class ThresholdForm(forms.ModelForm):
    class Meta:
        model = Threshold
        fields = ['value']
        # Form for Threshold model to configure reorder threshold for an item
        
    def clean_value(self):
        # Custom cleaning method for the value field
        value = self.cleaned_data.get('value')

        # Check if value is less than 1
        if value < 1:
            raise forms.ValidationError('Reorder threshold must be a positive integer.')

        return value

    

