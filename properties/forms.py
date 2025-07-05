# my_real_estate_site/properties/forms.py
from django import forms
from .models import Inquiry

class InquiryForm(forms.ModelForm):
    # Note: No specific styling attributes here, just basic Django widgets
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20, required=False)
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'message', 'property']
        widgets = {
            'property': forms.HiddenInput(), # Hide the property field on the form
        }