from django import forms
from .models import *
from django.core.exceptions import ValidationError


class NewOutboxForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewOutboxForm, self).__init__(*args, **kwargs)
        self.fields['agreementer'].queryset = Person.objects.filter(can_agree=True)
        self.fields['signatory'].queryset = Person.objects.filter(can_sign=True)
        # self.fields['signatory'].empty_label = None
        # self.fields['address'].empty_label = None
        # self.fields['recepient'].empty_label = None

    class Meta:
        model = Doc
        fields = [
            'title',
            'agreementer',
            'signatory',
            'address',
            'recepient',
            'docfile',
        ]
        widgets = {
            'title': forms.Textarea(attrs={'class':'form-control'}),
            'agreementer': forms.Select(attrs={'class':'form-control'}),
            'signatory': forms.Select(attrs={'class':'form-control'}),
            'address': forms.Select(attrs={'class':'form-control'}),
            'recepient': forms.Select(attrs={'class':'form-control'}),
            'docfile': forms.FileInput(attrs={'class':'form-control'}),
        }

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
    
