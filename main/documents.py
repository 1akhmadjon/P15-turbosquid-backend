from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Products


@registry.register_document
class DocumentProduct(Document):
    class Index:
        name = 'main'
        search = {'number_of_shards': 1, 'number_of_replicas': 0}

    title = fields.TextField(
        attr='title',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        })
    slug = fields.TextField(
        attr='slug',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        })
    description = fields.TextField(
        attr='description',
        fields={
            'raw': fields.TextField()
        })
    price = fields.FloatField(
        attr='price',
        fields={
            'raw': fields.FloatField()
        })

    class Django:
        model = Products
