from django import forms

from .models import UserFile


class UserFileForm(forms.ModelForm):
    class Meta:
        model = UserFile
        fields = ["file"]


class UserFileFilterForm(forms.Form):
    categories = [
        ("all", "All"),
        ("image", "Image"),
        ("video", "Video"),
        ("document", "Document"),
        ("zip", "zip"),
        ("other", "other"),
    ]
    categories = forms.MultipleChoiceField(
        choices=categories,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "select-all-checkbox"}),
    )
