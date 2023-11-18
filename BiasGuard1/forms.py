from django import forms
from .models import *


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('title', 'description', 'salary', 'education_level', 'city')