from django import forms


from .models import PhoneNumber


class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ("phone_number",)


class DOBIntervalForm(forms.Form):
    interval = forms.IntegerField()
    widgets = {"interval": forms.NumberInput(attrs={"type": "number"})}
