import requests
from django import forms
from django.core.exceptions import ValidationError

from . import views


class SearcCityForm(forms.Form):
    weather_city = forms.CharField(label="Місто", required=False)

    def clean_weather_city(self):
        weather_city = self.cleaned_data["weather_city"]
        if weather_city == "":
            return weather_city
        clean_url_weather = views.url_weather + weather_city.lower()
        response = requests.get(clean_url_weather)
        if response.status_code != 200:
            raise ValidationError("Введіть коректне ім'я міста.")
        return weather_city
