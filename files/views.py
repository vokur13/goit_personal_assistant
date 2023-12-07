from cloudinary import uploader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView, DetailView

from files.forms import UserFileForm, UserFileFilterForm
from files.models import UserFile


class UserFileListView(LoginRequiredMixin, ListView, FormView):
    """

    UserFileListView

    Subclass of LoginRequiredMixin, ListView, and FormView.

    Handles the display and filtering of UserFile objects for a specific user.

    Attributes:
    - model (class): The UserFile model class.
    - template_name (str): The name of the template to render.
    - success_url (str): The URL to redirect to after a successful form submission.

    Methods:
    - render_form(request, form, file_list=None): Renders the form and returns the rendered template with the form and optional file list.
        Parameters:
            - request (HttpRequest): The HTTP request object.
            - form (UserFileFilterForm): The form to render.
            - file_list (QuerySet, optional): The list of UserFile objects to include in the context. Default is None.
        Returns:
            - HttpResponse: The rendered template containing the form and file list, if provided.

    - filter_files(form): Filters the UserFile objects based on the selected categories in the form.
        Parameters:
            - form (UserFileFilterForm): The form containing the selected categories.
        Returns:
            - QuerySet: The filtered UserFile objects.

    - get(request, *args, **kwargs): Handles the GET request.
        Parameters:
            - request (HttpRequest): The HTTP request object.
            - args (tuple): Additional positional arguments.
            - kwargs (dict): Additional keyword arguments.
        Returns:
            - HttpResponse: The rendered form template.

    - post(request, *args, **kwargs): Handles the POST request.
        Parameters:
            - request (HttpRequest): The HTTP request object.
            - args (tuple): Additional positional arguments.
            - kwargs (dict): Additional keyword arguments.
        Returns:
            - HttpResponse: The rendered form template with the filtered file list, if the form is valid;
                            otherwise, the rendered form template without any file list.
    """

    model = UserFile
    template_name = "files/file_list.html"
    success_url = reverse_lazy("files:file_list")

    def render_form(self, request, form, file_list=None):
        context = {"form": form}
        if file_list is not None:
            context["file_list"] = file_list
        return render(request, self.template_name, context)

    def filter_files(self, form):
        category = form.cleaned_data["categories"]
        queryset = self.model.objects.filter(owner=self.request.user)
        if "all" not in category:
            queryset = queryset.filter(category__in=category)
        return queryset

    def get(self, request, *args, **kwargs):
        form = UserFileFilterForm()
        return self.render_form(request, form)

    def post(self, request, *args, **kwargs):
        form = UserFileFilterForm(request.POST)
        if form.is_valid():
            queryset = self.filter_files(form)
            return self.render_form(request, form, queryset)
        return self.render_form(request, form)


def get_user_file_form():
    return UserFileForm()


def get_and_validate_user_file_form(request):
    return UserFileForm(request.POST, request.FILES)


def upload_file_to_cloudinary(file_):
    return uploader.upload(file_, overwrite=True)


class UserFileUploadView(LoginRequiredMixin, View):
    template_name = "files/file_upload.html"
    success_url = reverse_lazy("files:file_list")

    def get(self, request):
        form = get_user_file_form()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = get_and_validate_user_file_form(request)

        if form.is_valid():
            file_ = form.cleaned_data["file"]
            cloudinary_response = upload_file_to_cloudinary(file_)
            return self.save_user_file_instance(form, request, cloudinary_response)
        else:
            return render(request, self.template_name, {"form": form})

    def save_user_file_instance(self, form, request, cloudinary_response):
        instance = form.save(commit=False)
        instance.category = instance.get_file_category()
        instance.file = cloudinary_response["secure_url"]
        instance.owner = self.request.user
        instance.save()

        return redirect(self.success_url)


class DownloadFileView(LoginRequiredMixin, DetailView):
    model = UserFile
    template_name = "files/download_file.html"
    success_url = reverse_lazy("files:file_list")

    CONTENT_DISPOSITION_HEADER = "Content-Disposition"
    X_ACCEL_REDIRECT_HEADER = "X-Accel-Redirect"

    def post(self, request, pk):
        user_file = get_object_or_404(UserFile, id=pk)

        cloudinary_url = user_file.file.url
        file_name = cloudinary_url.split("/")[-1]

        response = HttpResponse()
        response[self.CONTENT_DISPOSITION_HEADER] = f"attachment; filename={file_name}"
        response[self.X_ACCEL_REDIRECT_HEADER] = cloudinary_url

        return response
