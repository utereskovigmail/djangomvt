from django.shortcuts import render, redirect
from django.contrib import messages
from categories.forms import CategoryForm
from django.utils.text import slugify

from categories.models import Category


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                category = form.save(commit=False)

                # призначаємо зображення, якщо воно є
                if 'image' in request.FILES:
                    category.image = request.FILES['image']

                # зберігаємо у базу даних
                category.save()

                messages.success(request, 'Категорію успішно створено!')
                return redirect('homepage')

            except Exception as e:
                messages.error(request, f"Щось пішло не так: {e}")
                return redirect('homepage')
        else:
            messages.error(request, 'Виправте помилки у формі')
    else:
        form = CategoryForm()

    return render(request, "add_category.html", {"form": form})

def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, "category_list.html", {
        "categories": categories
    })