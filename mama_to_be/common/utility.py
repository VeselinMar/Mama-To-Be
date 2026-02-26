import os
import uuid
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image, UnidentifiedImageError

WEBP_QUALITY = 92

def process_image_to_webp(image_field, webp_quality=WEBP_QUALITY):
    """
    Processes an uploaded image:
    - Converts to WebP
    - Returns a Django ContentFile ready for saving
    """
    try:
        with Image.open(image_field) as img:
            img.verify()
    except UnidentifiedImageError:
        raise ValueError("Uploaded file is not a valid image")
    
    with Image.open(image_field) as img:

        buffer = BytesIO()
        use_lossless = image_field.name.lower().endswith(".png")
        img.save(
            buffer,
            format="WEBP",
            quality=webp_quality,
            lossless=use_lossless,
            method=6,
            optimize=True
        )

    base_name = os.path.splitext(os.path.basename(image_field.name))[0]
    new_name = f"articles/{base_name}-{uuid.uuid4().hex}.webp"

    return ContentFile(buffer.getvalue(), name=new_name)