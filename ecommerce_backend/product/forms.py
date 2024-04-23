from django import forms
from django.core.exceptions import ValidationError

from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'category', 'brand', 'price', 'discount_price', 'stock', 'attachments', 'is_deleted')
    
    def clean(self):
        attachments = self.cleaned_data.get('attachments')

        if attachments and attachments.count() > 5:
            raise ValidationError('Maximum 5 attachments are allowed.')
        
        return self.cleaned_data