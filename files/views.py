import cloudinary.uploader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView

from files.forms import UserFileForm, UserFileFilterForm
from files.models import UserFile


class UserFileListView(LoginRequiredMixin, ListView, FormView):
    model = UserFile
    template_name = "files/file_list.html"  # Replace with your actual template path
    success_url = reverse_lazy("files:file_list")

    def get(self, request, *args, **kwargs):
        form = UserFileFilterForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserFileFilterForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data["categories"]
            queryset = UserFile.objects.get_queryset().filter(owner=self.request.user)
            if "all" not in category:
                queryset = queryset.filter(category__in=category)
            return render(
                request,
                self.template_name,
                {"form": form, "file_list": queryset},
            )
        return render(request, self.template_name, {"form": form})


class UserFileUploadView(LoginRequiredMixin, View):
    template_name = "files/file_upload.html"
    success_url = reverse_lazy("files:file_list")

    def get(self, request):
        form = UserFileForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = UserFileForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)

            # Upload the file to Cloudinary
            file = form.cleaned_data["file"]
            cloudinary_response = cloudinary.uploader.upload(file)

            # Determine the category based on file type
            category = self.get_file_category(file.name)
            instance.category = category
            instance.file = cloudinary_response["secure_url"]
            instance.owner = self.request.user
            instance.save()

            return redirect(self.success_url)

        return render(request, self.template_name, {"form": form})

    def get_file_category(self, filename):
        extension = filename.split(".")[-1].lower()

        if extension in ["jpg", "jpeg", "png", "gif"]:
            return "image"
        elif extension in ["mp4", "mov", "avi"]:
            return "video"
        elif extension in ["pdf", "doc", "docx", "txt"]:
            return "document"
        elif extension == "zip":
            return "zip"
        else:
            return "other"
