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
            'name': forms.TextInput(),
            'text': forms.Textarea(),
        }