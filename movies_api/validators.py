from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.conf import settings
import os

def validate_file_size(value):
    filesize = value.size
    name, extension = os.path.splitext(value.name)
    image_extensions = ['.jpg', '.jpeg', '.png']
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv']
    
    if extension.lower() in image_extensions:
        if filesize > settings.MAX_POSTER_SIZE:
            raise ValidationError(f"Maximum image size allowed is {settings.MAX_POSTER_SIZE // (1024*1024)}MB")
    elif extension.lower() in video_extensions:
        if filesize > settings.MAX_UPLOAD_SIZE:
            raise ValidationError(f"Maximum video size allowed is {settings.MAX_UPLOAD_SIZE // (1024*1024)}MB")

poster_validator = FileExtensionValidator(
    allowed_extensions=['jpg', 'jpeg', 'png'],
    message="Only JPG, JPEG and PNG image formats are allowed"
)

trailer_validator = FileExtensionValidator(
    allowed_extensions=['mp4', 'mov', 'avi', 'mkv'],
    message="Only MP4, MOV, AVI and MKV video formats are allowed"
)
