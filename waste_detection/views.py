from django.shortcuts import render

# Create your views here.
from .form import WasteImageForm
from .models import WasteImage
from PIL import Image
import os

#importation pour la visualisation 
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse
from .models import WasteImage


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


def basic_stats(request):
    # Ce code sert à compter les annotations 
    pleines = WasteImage.objects.filter(annotation='pleine').count()
    vides = WasteImage.objects.filter(annotation='vide').count()

    # Cela permet de créer un graphe en barres
    fig, ax = plt.subplots()
    ax.bar(['Pleine', 'Vide'], [pleines, vides], width=0.5)
    ax.set_title("Répartition des annotations")

    # Ici, le graphe est gardé en mémoire (PNG)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')