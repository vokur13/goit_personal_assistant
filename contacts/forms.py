from django import forms


from .models import PhoneNumber


class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ("phone_number",)


class DOBIntervalForm(forms.Form):
    interval = forms.IntegerField()
    widgets = {"interval": forms.NumberInput(attrs={"type": "number"})}


class SearcListForm(forms.Form):
    search = forms.CharField(label="Прізвище", required=False)
    search_name = forms.CharField(label="Ім'я", required=False)
