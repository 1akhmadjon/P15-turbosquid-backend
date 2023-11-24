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
    name = models.CharField(max_length=200, blank=True, null=True)


class Format(models.Model):
    format = models.CharField(max_length=100, blank=True, null=True)


class Products(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, blank=True, null=True)
    format = models.ForeignKey('Format', on_delete=models.CASCADE, blank=True, null=True)

    def save(
            self, *args, **kwargs
    ):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Products'
        verbose_name_plural = 'Products'


class Shoppingcart(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id


class Image(models.Model):
    image = models.ImageField(upload_to=slugify_upload, blank=True, null=True)
    product = models.ForeignKey('Products', on_delete=models.CASCADE)


class UserBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=10000)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title


class ArchiveShoppingcart(models.Model):
    product = models.ForeignKey(Shoppingcart, on_delete=models.CASCADE)
    user = models.ForeignKey(Shoppingcart, on_delete=models.CASCADE)


class Comment(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True, null=True)


class Subscription(models.Model):
    email = models.EmailField()
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
 

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
