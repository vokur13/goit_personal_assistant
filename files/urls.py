from django.urls import path

from .views import UserFileListView, UserFileUploadView

app_name = "files"

urlpatterns = [
    path("", UserFileListView.as_view(), name="file_list"),
    path("upload/", UserFileUploadView.as_view(), name="file_upload"),
]
