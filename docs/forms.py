from django import forms
from .models import *


class NewOutboxForm(forms.Form):
    title = forms.CharField(
        max_length=150,
        label='Краткое содержание',
        widget=forms.Textarea(attrs={'class':'form-control'})
    )
    docfile = forms.FileField(
        allow_empty_file=True,
        label='Вложение',
        widget=forms.FileInput(attrs={'class':'form-control'})
    )
    signatory = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        empty_label=None,
        label='Подписант',
        widget=forms.Select(attrs={'class':'form-control'})
    )
