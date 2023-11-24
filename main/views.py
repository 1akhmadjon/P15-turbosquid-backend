from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from main.models import Products, Shoppingcart
from .serializers import ProductSerializer, ShoppingcartSerializers


class ProductAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = ProductSerializer

    def get(self, request):
        todos = Products.objects.all()
        todos_data = ProductSerializer(todos, many=True)
        return Response(todos_data.data)


class AddProductView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        product_serializer = ProductSerializer(data=request.data)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        return Response(product_serializer.data)


class ProductDetailAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = ProductSerializer

    def get(self, request, slug):
        try:
            todo = Products.objects.get(slug=slug)
        except Products.DoesNotExist:
            return Response({'success': False}, status=404)
        todo_serializer = ProductSerializer(todo)
        return Response(todo_serializer.data)

class ShoppingcartAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user_id = request.user.id
        shoppingcart = Shoppingcart.objects.filter(user_id_id=user_id)
        shoppingcart_serializers = ShoppingcartSerializers(shoppingcart, many=True)
        return Response(shoppingcart_serializers.data)

class AddShoppingcartAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        user_id = request.user.id
        product_id = request.POST.get('product_id')
        if Shoppingcart.objects.filter(Q(user_id_id=user_id) & Q(product_id_id=product_id)).exists():
            shoppingcart = Shoppingcart.objects.get(Q(user_id_id=user_id) & Q(product_id_id=product_id))
            shoppingcart_serializers = ShoppingcartSerializers(shoppingcart)
            return Response(shoppingcart_serializers.data)
        else:
            shoppingcart = Shoppingcart.objects.create(
                product_id_id=product_id,
                user_id_id=user_id
            )
            shoppingcart.save()
            shoppingcart_serializers = ShoppingcartSerializers(shoppingcart)
            print(shoppingcart_serializers.data)
            return Response(shoppingcart_serializers.data)









