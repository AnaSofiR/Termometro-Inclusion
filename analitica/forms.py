from django import forms
from BiasGuard1.models import *

class JobRatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('rating',)
