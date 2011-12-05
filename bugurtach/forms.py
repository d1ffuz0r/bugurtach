# -*- coding: utf-8 -*-
from bugurtach.models import Bugurt, Tag, Proof
from django import forms


prepare = lambda string: filter(
    lambda val: val != u'', string.replace(" ", "").split(",")
)


class AddBugurt(forms.ModelForm):
    class Meta:
        model = Bugurt
        fields = ("name", "text", "author")
        widgets = {
            "name": forms.TextInput({"required": True}),
            "text": forms.Textarea({"required": True}),
            "author": forms.HiddenInput()
        }

    def clean(self):
        tags = set(prepare(self.data["tags"]))
        proofs = set(prepare(self.data["proofs"]))
        if not tags:
            raise forms.ValidationError("Введи тег(и)")
        if not proofs:
            raise forms.ValidationError("Введи пруф(ы)")
        self.cleaned_data["tags"] = tags
        self.cleaned_data["proofs"] = proofs
        return self.cleaned_data

    def save(self, commit=True):
        data = self.cleaned_data
        super(AddBugurt, self).save()

        tags = data["tags"]
        proofs = data["proofs"]

        if tags and proofs:
            bugurt = Bugurt.objects.get(pk=self.instance.pk)
            for name in tags:
                    t, created = Tag.objects.get_or_create(title=name)
                    bugurt.bugurttags_set.create(bugurt=bugurt, tag=t)
            for link in proofs:
                    p, created = Proof.objects.get_or_create(link=link)
                    bugurt.bugurtproofs_set.create(bugurt=bugurt, proof=p)
        return data


class EditBugurt(forms.ModelForm):
    class Meta:
        model = Bugurt
        fields = ("name", "text")
        widgets = {
            "name": forms.TextInput(attrs={"style": "margin-bottom:10px;",
                                           "size": 77}),
            "text": forms.Textarea(attrs={"style": "margin-left:42px;",
                                          "cols": 60,
                                          "rows": 20}),
        }


class AddTag(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(
        attrs={"title": "Одно название тега"})
    )


class AddProof(forms.Form):
    link = forms.CharField(label="", widget=forms.TextInput(
        attrs={"title": "Один линк пруфа"})
    )
