from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_image, name='upload_image'),
    path('stats/', views.basic_stats, name='basic_stats'),

]
