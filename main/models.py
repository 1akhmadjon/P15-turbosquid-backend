from os.path import splitext
from django.contrib.auth.views import get_user_model
from django.db import models
from django.template.defaultfilters import slugify

from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


def slugify_upload(instance, filename):
    folder = instance._meta.model_name
    name, ext = splitext(filename)
    name_t = slugify(name) or name
    return f"{folder}/{name_t}{ext}"


# This Model created for sections filtered by types like [3d models, free 3d models, 3ds max models etc.]
class Sections(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


# This Model for sections at main page like [cars, characters, animals, vehicles, etc.] using MPTTModel
class Category(MPTTModel):
    name = models.CharField(max_length=255)
    section = models.ForeignKey(Sections, on_delete=models.CASCADE, blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class ProductType(models.Model):
    name = models.CharField(max_length=200)


class Products(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)

    def save(
            self, *args, **kwargs
    ):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Shoppingcart(models.Model):
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id


class Image(models.Model):
    image = models.ImageField(upload_to=slugify_upload, blank=True, null=True)
    product = models.ForeignKey('Products', on_delete=models.CASCADE)


class Subscription(models.Model):
    email = models.EmailField()
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
 