from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


def resize_image(image, size=(600, 600)):
    """
    Изменяет размер изображения до заданного размера (600x600 пикселей).
    """
    img = Image.open(image)
    img = img.convert("RGB")  # Преобразуем в RGB, если это необходимо
    img = img.resize(size, Image.LANCZOS)  # Изменяем размер до 600x600 пикселей

    # Сохраняем измененное изображение в буфер
    output = BytesIO()
    img.save(output, format='JPEG', quality=85)
    output.seek(0)

    # Возвращаем измененное изображение в виде ContentFile
    return ContentFile(output.read(), name=image.name)
