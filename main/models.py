from os.path import splitext

from django.db import models
from django.template.defaultfilters import slugify

from mptt.models import MPTTModel, TreeForeignKey


def slugify_upload(instance, filename):
    folder = instance._meta.model_name
    name, ext = splitext(filename)
    name_t = slugify(name) or name
    return f"{folder}/{name_t}{ext}"


class Image(models.Model):
    image = models.ImageField(upload_to=slugify_upload, blank=True, null=True)
    product = models.ForeignKey('Products', on_delete=models.CASCADE)


class Products(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    price = models.IntegerField()
    upload_at = models.DateTimeField(auto_now_add=True)

    def save(
            self, *args, **kwargs
    ):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# This Model created for sections filtered by types like [3d models, free 3d models, 3ds max models etc.]
class SectionsByType(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


# This Model for sections at main page like [cars, characters, animals, vehicles, etc.] using MPTTModel
class Sections(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
