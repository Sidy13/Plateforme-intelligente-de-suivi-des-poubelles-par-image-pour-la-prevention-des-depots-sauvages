from django.db import models

# Create your models here.
class WasteImage(models.Model):
    image = models.ImageField(upload_to='images/')
    date_added = models.DateTimeField(auto_now_add=True)
    annotation = models.CharField(max_length=10, choices=[('pleine', 'Pleine'), ('vide', 'Vide')], blank=True, null=True)

    # Métadonnées simples
    file_size_kb = models.FloatField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    avg_red = models.IntegerField(null=True, blank=True)
    avg_green = models.IntegerField(null=True, blank=True)
    avg_blue = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Image {self.id} - {self.annotation or 'Non annotée'}"