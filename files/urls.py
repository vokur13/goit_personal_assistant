from django.urls import path

from .views import UserFileListView, UserFileUploadView, DownloadFileView

app_name = "files"

urlpatterns = [
    path("", UserFileListView.as_view(), name="file_list"),
    path("upload/", UserFileUploadView.as_view(), name="file_upload"),
    path("download/<int:pk>/", DownloadFileView.as_view(), name="download_file"),
]
