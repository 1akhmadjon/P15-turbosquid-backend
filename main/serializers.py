from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers

from .documents import DocumentProduct
from .models import Products, Shoppingcart, Subscription
from .tasks import send_email


class ProductSerializerForRetrieve(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        subscribers = Subscription.objects.all().values('email')
        subscriber_emails = [email['email'] for email in list(subscribers)]
        product = Products.objects.create(**validated_data)
        product_serializer = ProductSerializerForRetrieve(product)
        send_email.delay(subscriber_emails, product_serializer.data)
        return product

    class Meta:
        model = Products
        fields = '__all__'


class ShoppingcartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Shoppingcart
        fields = '__all__'


class ProductDocumentSerializer(DocumentSerializer):
    price = serializers.FloatField()

    def get_price(self, obj):
        return float(obj.price)

    class Meta:
        document = DocumentProduct
        fields = ('title', 'slug', 'description', 'price')


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
