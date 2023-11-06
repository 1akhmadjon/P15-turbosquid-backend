from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


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
