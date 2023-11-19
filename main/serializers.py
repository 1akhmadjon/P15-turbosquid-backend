from rest_framework import serializers
from .models import Products, Shoppingcart, Category, Sections, Subscribers
from .tasks import send_email


class ProductSerializerForRetrieve(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        subscribers = Subscribers.objects.all().values('email')
        subscriber_emails = [email['email'] for email in list(subscribers)]
        print(subscriber_emails)
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


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sections
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class QuerySerializer(serializers.Serializer):
    query = serializers.CharField()
