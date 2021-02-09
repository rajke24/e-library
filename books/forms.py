from django import forms
from .models import Opinion


class OpinionCreateForm(forms.ModelForm):
    class Meta:
        model = Opinion
        fields = ['title', 'content', 'rating']
