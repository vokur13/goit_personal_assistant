import cloudinary.uploader

from django_project.settings import env

# Replace 'your_cloud_name', 'your_api_key', and 'your_api_secret' with your Cloudinary credentials
cloud_name = env.str("CLOUD_NAME")
api_key = env.str("API_KEY")
api_secret = env.str("API_SECRET")

# Set Cloudinary configuration
cloudinary.config(cloud_name=cloud_name, api_key=api_key, api_secret=api_secret)

# Replace 'custom_public_id' with your desired custom public ID
custom_public_id = "custom_public_id"

# Specify the file you want to upload
file_to_upload = "/Users/vokur/PycharmProjects/djangoProject/personal_assistant/django_project/media/images/24559-1-shrek-photos.jpeg"

# Upload the file to Cloudinary with the custom public ID
result = cloudinary.uploader.upload(file_to_upload, public_id=custom_public_id)

# Print the result, including the public ID assigned by Cloudinary
print(result)
