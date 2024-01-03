from django import forms
from datetime import *

from .models import Hotel, HotelImage

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ["name", "address", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input-style"}),
            "address": forms.TextInput(attrs={"class": "input-style"}),
            "description": forms.Textarea(attrs={"class": "input-style"}),
        }


class HotelImageForm(forms.ModelForm):
    class Meta:
        model = HotelImage
        fields = ["hotel", "hotel_images"]


HotelImageFormSet = forms.inlineformset_factory(
    Hotel, HotelImage, form=HotelImageForm, extra=1, can_delete=True
)
