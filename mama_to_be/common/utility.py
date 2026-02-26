import os
import uuid
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image, UnidentifiedImageError

WEBP_QUALITY = 92
MAX_WIDTH = 1200
MAX_HEIGHT = 1200

def process_image_to_webp(
    image_field,
    webp_quality=WEBP_QUALITY,
    max_width=MAX_WIDTH,
    max_height=MAX_HEIGHT
):
    try:
        with Image.open(image_field) as img:
            img.verify()
    except UnidentifiedImageError:
        raise ValueError("Uploaded file is not a valid image")

    image_field.seek(0)

    with Image.open(image_field) as img:
        original_width, original_height = img.size

        if original_width > max_width or original_height > max_height:
            img.thumbnail(
                (max_width, max_height),
                Image.Resampling.LANCZOS
            )

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
    new_name = f"{base_name}-{uuid.uuid4().hex}.webp"

    return ContentFile(buffer.getvalue(), name=new_name)