from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('exchange_rates/', views.rates, name='rates'),
    path('weather/', views.weather, name='weather'),
    path('<str:category>/', views.show, name='show'),    
]
