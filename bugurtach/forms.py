# -*- coding: utf-8 -*-
from bugurtach.models import Bugurt
from django import forms

class AddBugurt(forms.ModelForm):
    class Meta:
        model = Bugurt
        fields = ('name', 'text', 'author')
        widgets = {
            'name': forms.TextInput({'required': True}),
            'text': forms.Textarea({'required': True}),
            'author': forms.HiddenInput()
        }

class EditBugurt(forms.ModelForm):
    class Meta:
        model = Bugurt
        fields = ('name', 'text')
        widgets = {
            'name': forms.TextInput(attrs={'style':'margin-bottom:10px;'}),
            'text': forms.Textarea(attrs={'style':'margin-left:42px;'}),
        }

class AddTag(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'title': 'Одно название тега'}))

class AddProof(forms.Form):
    link = forms.CharField(label="", widget=forms.TextInput(attrs={'title': 'Один линк пруфа'}))
