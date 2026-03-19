from categories.models import Category
from django.db import models
from PIL import Image
import uuid
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils.text import slugify

class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True,related_name="images")
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    priority = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["priority", "created_at"]

    def __str__(self):
        return f"Фото [{self.priority}] для {self.product.name}"

class TempImage(models.Model):
    image = models.ImageField(upload_to='temp/')

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)

            # convert to RGB (needed for WEBP)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # compress + convert to WEBP
            output = BytesIO()
            img.save(output, format='WEBP', quality=75)  # adjust quality here

            output.seek(0)

            # generate new filename
            new_filename = f"{uuid.uuid4()}.webp"

            # replace image
            self.image.save(new_filename, ContentFile(output.read()), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Temp {self.id}"