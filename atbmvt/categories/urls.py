from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('add/', views.add_category, name="add"),
    path('', views.category_list, name='category_list'),
]