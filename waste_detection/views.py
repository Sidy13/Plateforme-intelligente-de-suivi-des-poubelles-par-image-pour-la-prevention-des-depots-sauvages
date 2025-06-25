from django.shortcuts import render

# Create your views here.
from .form import WasteImageForm
from .models import WasteImage
from PIL import Image
import os

def upload_image(request):
    last_image = None
    if request.method == 'POST':
        form = WasteImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            # Extraction de caractéristiques
            image_path = instance.image.path
            pil_image = Image.open(image_path)
            instance.width, instance.height = pil_image.size
            instance.file_size_kb = os.path.getsize(image_path) / 1024

            pixels = list(pil_image.getdata())
            r_total = sum(p[0] for p in pixels)
            g_total = sum(p[1] for p in pixels)
            b_total = sum(p[2] for p in pixels)
            pixel_count = len(pixels)

            instance.avg_red = r_total // pixel_count
            instance.avg_green = g_total // pixel_count
            instance.avg_blue = b_total // pixel_count

            instance.save()
            last_image = instance
    else:
        form = WasteImageForm()

    return render(request, 'upload.html', {'form': form, 'last_image': last_image})