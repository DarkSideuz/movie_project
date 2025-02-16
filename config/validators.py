from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
import magic

def validate_file_size(value):
    filesize = value.size
    
    if filesize > 10 * 1024 * 1024:  # 10MB
        raise ValidationError("Maximum file size is 10MB")

def poster_validator(image):
    # Fayl turi tekshiruvi
    file_type = magic.from_buffer(image.read(1024), mime=True)
    if file_type not in ['image/jpeg', 'image/png']:
        raise ValidationError("Only JPEG and PNG files are allowed")
    
    # O'lcham tekshiruvi
    width, height = get_image_dimensions(image)
    if width < 300 or height < 450:
        raise ValidationError("Minimum image dimensions are 300x450 pixels")
    
    # Fayl hajmi tekshiruvi
    if image.size > 5 * 1024 * 1024:  # 5MB
        raise ValidationError("Maximum file size is 5MB")

def trailer_validator(video):
    # Fayl turi tekshiruvi
    file_type = magic.from_buffer(video.read(1024), mime=True)
    if file_type not in ['video/mp4', 'video/quicktime']:
        raise ValidationError("Only MP4 and MOV files are allowed")
    
    # Fayl hajmi tekshiruvi
    if video.size > 100 * 1024 * 1024:  # 100MB
        raise ValidationError("Maximum file size is 100MB")
