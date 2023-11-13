from rest_framework import serializers

from .models import Products, Shoppingcart


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class ShoppingcartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Shoppingcart
        fields = '__all__'