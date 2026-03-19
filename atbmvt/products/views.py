import os

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import ProductImage, TempImage, Product
from django.views.decorators.csrf import csrf_exempt
from .forms import ProductForm
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.http import JsonResponse
import uuid


# Create your views here.


def upload_temp_image(request):
    if request.method == "POST":
        file = request.FILES.get('filepond')

        print("FILES:", request.FILES)  # DEBUG
        print("file:", file)

        if not file:
            return JsonResponse({"error": "No file received"}, status=400)

        temp = TempImage.objects.create(image=file)

        return JsonResponse({"file_id": temp.id})


def delete_temp_image(request):
    if request.method == "DELETE":
        import json

        data = json.loads(request.body)
        print("data:", data)
        file_id = data

        try:
            temp = TempImage.objects.get(id=file_id)
            temp.delete()
            return JsonResponse({"status": "ok"})
        except TempImage.DoesNotExist:
            return JsonResponse({"status": "error"})


def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save()

            images = request.POST.getlist('uploaded_images')
            priorities = request.POST.getlist('priorities')

            for img_id, priority in zip(images, priorities):
                temp = TempImage.objects.get(id=img_id)

                temp.image.open()
                content = temp.image.read()

                filename = os.path.basename(temp.image.name)

                ProductImage.objects.create(
                    product=product,
                    image=ContentFile(content, name=filename),
                    priority = int(priority)
                )

                temp.delete()

            return redirect('homepage')

    else:
        form = ProductForm()

    return render(request, "add_product.html", {"form": form})

def list_products(request):
    products = Product.objects.prefetch_related('images').order_by('category__name')
    return render(request, "list_products.html", {"products": products})

def edit_product(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            product = form.save()

            # 🔥 NEW uploaded images (from FilePond)
            images = request.POST.getlist('uploaded_images')

            product.images.all().delete()

            for img_id in images:
                temp = TempImage.objects.get(id=img_id)

                ProductImage.objects.create(
                    product=product,
                    image=ContentFile(
                        temp.image.read(),
                        name=os.path.basename(temp.image.name)
                    )
                )

                temp.delete()

            return redirect('/products/')

    else:
        form = ProductForm(instance=product)

    return render(request, "edit_product.html", {
        "form": form,
        "product": product
    })

@require_POST
def delete_product(request, slug):
    product = get_object_or_404(Product, slug=slug)

    for img in product.images.all():
        img.image.delete(save=False)

    product.delete()
    return redirect('products:list_products')