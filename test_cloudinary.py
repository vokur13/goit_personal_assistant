import cloudinary
from cloudinary import api

from django_project.settings import env

# Replace 'your_cloud_name', 'your_api_key', and 'your_api_secret' with your Cloudinary credentials
cloud_name = env.str("CLOUD_NAME")
api_key = env.str("API_KEY")
api_secret = env.str("API_SECRET")

# Set Cloudinary configuration
cloudinary.config(cloud_name=cloud_name, api_key=api_key, api_secret=api_secret)

api.create_folder("media/downloads")

# uploader.upload(‘local path or online url of the file to be uploaded', folder = “_______/”, public_id = “_____”)
