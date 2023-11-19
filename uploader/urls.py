from django.urls import path
from .views import upload_file, file_list


urlpatterns = [
    path('', upload_file, name='upload_file'),
    path('file_list/', file_list, name='file_list'),

]
