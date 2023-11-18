import os
from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import File
from django.conf import settings
from django.http import HttpResponse
import cloudinary.uploader
from cloudinary.api import resources
# from cloudinary.uploader import upload

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        file_type = request.POST.get('file_type')

        if file_type == 'image':
            cloudinary.uploader.upload(file, resource_type="image")
        elif file_type == 'video':
            cloudinary.uploader.upload(file, resource_type="video")
        elif file_type == 'document':
            cloudinary.uploader.upload(file, resource_type="raw")

    return render(request, 'upload_file.html')

def file_list(request):
    # Отримати файли з моделі File
    local_files = File.objects.all()

    # Отримати файли з Cloudinary API
    cloudinary_files = resources(type="upload", prefix="user_uploads/")['resources']

    # Витягти тільки публічні URL з Cloudinary
    cloudinary_urls = [file['secure_url'] for file in cloudinary_files if 'secure_url' in file]

    # Створити об'єкти File для файлів з Cloudinary
    cloudinary_files_objects = [File(file=cloudinary_url) for cloudinary_url in cloudinary_urls]

    # Об'єднати файли з обох джерел
    all_files = list(local_files) + cloudinary_files_objects

    # Сортувати файли за категоріями (розширенням)
    images = [file for file in all_files if file.file.name.lower().endswith(('.jpg', '.png', '.gif', '.jpeg'))]
    documents = [file for file in all_files if file.file.name.lower().endswith(('.pdf', '.doc', '.docx', '.txt'))]
    videos = [file for file in all_files if file.file.name.lower().endswith(('.mp4', '.avi', '.mkv'))]

    return render(request, 'file_list.html', {'images': images, 'documents': documents, 'videos': videos})

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

# def upload_to_cloudinary(request):
#     if request.method == 'POST':
#         # Отримайте файл з запиту Django
#         uploaded_file = request.FILES['file']

#         # Конфігурація Cloudinary (вкажіть ваші ключі)
#         cloudinary.config(
#             cloud_name="dwu51daym",
#             api_key="419691218689934",
#             api_secret="1zbqd9f1ptwFtG1yEAGuoCuLXUQ" 
#         )

#         # Параметри завантаження, такі як папка в Cloudinary
#         folder_name = "Images"  # Вкажіть свою папку
#         response = upload(uploaded_file, folder=folder_name)

#         # URL завантаженого файлу в Cloudinary
#         file_url = response['secure_url']
#         return HttpResponse(f"File uploaded to: {file_url}")

#     return render(request, 'upload_form.html')