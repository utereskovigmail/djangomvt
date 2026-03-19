from django.urls import path
from . import views

app_name='products'

urlpatterns = [
    path('add/', views.create_product, name='add'),
    path('upload-temp/', views.upload_temp_image, name='upload-temp'),
    path('delete-temp/', views.delete_temp_image, name='delete-temp'),
    path('', views.list_products, name='list_products'),
    path('edit/<slug:slug>/', views.edit_product, name='edit'),
    path('delete/<slug:slug>/', views.delete_product, name='delete'),

]