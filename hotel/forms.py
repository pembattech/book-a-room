from django import forms
from django.core.exceptions import ValidationError
from datetime import *

from .models import Hotel, HotelImage, Reservation


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ["name", "address", "description", "price"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input-style"}),
            "address": forms.TextInput(attrs={"class": "input-style"}),
            "description": forms.Textarea(attrs={"class": "input-style"}),
            "price": forms.TextInput(
                attrs={"class": "input-style", "type": "number", "step": "0.01"}
            ),
        }
        
    def __init__(self, *args, **kwargs):
        super(HotelForm, self).__init__(*args, **kwargs)
        # Make the 'price' field not required
        self.fields["price"].required = False

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get("price")

        if price is not None and price < 0:
            raise forms.ValidationError("Price must be a non-negative value")

        return cleaned_data


class HotelImageForm(forms.ModelForm):
    class Meta:
        model = HotelImage
        fields = ["hotel", "hotel_images"]


HotelImageFormSet = forms.inlineformset_factory(
    Hotel, HotelImage, form=HotelImageForm, extra=1, can_delete=True
)


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["check_in_date", "check_out_date"]

        widgets = {
            "check_in_date": forms.DateInput(
                attrs={"type": "date", "class": "input-check_in"}
            ),
            "check_out_date": forms.DateInput(
                attrs={"type": "date", "class": "input-check_out"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)

        # Set default values for check-in and check-out dates
        today = date.today()
        tomorrow = today + timedelta(days=1)

        self.fields["check_in_date"].initial = today
        self.fields["check_out_date"].initial = tomorrow

    def clean_check_in_date(self):
        check_in_date = self.cleaned_data.get("check_in_date")

        # Check if check-in date is in the past
        if check_in_date < date.today():
            raise ValidationError("Check-in date must be in the future.")

        return check_in_date

    def clean(self):
        super().clean()

        # Ensure check-out date is after check-in date
        check_in_date = self.cleaned_data.get("check_in_date")
        check_out_date = self.cleaned_data.get("check_out_date")

        if check_out_date <= check_in_date:
            raise ValidationError("Check-out date must be after check-in date.")

        return self.cleaned_data
