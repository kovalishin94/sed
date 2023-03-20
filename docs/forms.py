from django import forms
from .models import *
from django.core.exceptions import ValidationError


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
        queryset=Person.objects.filter(can_sign=True),
        empty_label=None,
        label='Подписант',
        widget=forms.Select(attrs={'class':'form-control'})
    )
    agreementer = forms.ModelChoiceField(
        queryset=Person.objects.filter(can_agree=True),
        empty_label=None,
        label='Согласующий',
        widget=forms.Select(attrs={'class':'form-control'})
    )
    address = forms.ModelChoiceField(
        queryset=Institution.objects.all(),
        empty_label=None,
        label='Адресат',
        widget=forms.Select(attrs={'class':'form-control'})
    )
    recepient = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        empty_label=None,
        label='Получатель',
        widget=forms.Select(attrs={'class':'form-control'})
    )

    def clean_recepient(self):
        signatory = self.cleaned_data['signatory']
        recepient = self.cleaned_data['recepient']
        agreementer = self.cleaned_data['agreementer']
        if signatory == recepient:
            raise ValidationError('Подписант не может быть адресатом')
        elif recepient == agreementer:
            raise ValidationError('Адресат не может быть согласующим')
        else:
            return recepient
    
