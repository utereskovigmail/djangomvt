from django.urls import path
from . import views

app_name='products'

urlpatterns = [
    path('add/', views.create_product, name='add'),
    path('upload-temp/', views.upload_temp_image, name='upload-temp'),
    path('delete-temp/', views.delete_temp_image, name='delete-temp'),
]