from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers

from .documents import DocumentProduct
from .models import (
    Products,
    Shoppingcart,
    Subscription,
    Sections,
    Category,
    Comment,
    Order,
    ProductType,
    Format,
    Like,
)
from .tasks import send_email


class ProductSerializerForRetrieve(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    product_type = ProductTypeSerializer()
    format = FormatSerializer()

    def create(self, validated_data):
        subscribers = Subscription.objects.all().values('email')
        subscriber_emails = [email['email'] for email in list(subscribers)]
        todo = Products.objects.create(**validated_data)
        todo_serializer = ProductSerializerForRetrieve(todo)
        send_email.delay(subscriber_emails, todo_serializer.data)
        return todo

    class Meta:
        model = Products
        fields = '__all__'


class ShoppingcartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Shoppingcart
        fields = '__all__'
        read_only_fields = ('user',)


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class ProductDocumentSerializer(DocumentSerializer):
    price = serializers.FloatField()

    def get_price(self, obj):
        return float(obj.price)

    class Meta:
        document = DocumentProduct
        fields = ('title', 'slug', 'description', 'price')


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sections
        fields = '__all__'


class QuerySerializer(serializers.Serializer):
    query = serializers.CharField()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user',)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ('user',)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('user',)
