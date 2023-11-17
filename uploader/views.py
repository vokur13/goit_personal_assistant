import os
from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import File
from django.conf import settings

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user
            file_instance.save()
            return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'upload_file.html', {'form': form})

def file_list(request):
    selected_category = request.GET.get('category', '')
    files = File.objects.filter(user=request.user)

    # Сортування за розширенням файлу
    files = files.order_by('extension', 'file')

    return render(request, 'file_list.html', {'files': files, 'selected_category': selected_category})


def organize_files(request):
    # Отримання усіх файлів користувача
    files = File.objects.filter(user=request.user)

    # Створення папок для різних розширень
    extensions = set([file.file.name.split('.')[-1] for file in files])
    for extension in extensions:
        folder_path = os.path.join(settings.MEDIA_ROOT, f'user_uploads_{extension}')
        os.makedirs(folder_path, exist_ok=True)

    # Переміщення файлів відповідно до їхнього розширення
    for file in files:
        extension = file.file.name.split('.')[-1]
        source_path = os.path.join(settings.MEDIA_ROOT, file.file.name)
        destination_path = os.path.join(settings.MEDIA_ROOT, f'user_uploads_{extension}', file.file.name)
        os.rename(source_path, destination_path)

    return redirect('file_list')
