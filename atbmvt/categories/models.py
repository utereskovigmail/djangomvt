from django.db import models
from PIL import Image
import os
import uuid
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, blank=True, null=True)

    image = models.ImageField(upload_to='categories/', blank=True, null=True)

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

        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            self.slug = slug

            counter = 1

            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name