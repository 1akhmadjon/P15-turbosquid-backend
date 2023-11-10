from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Products
from main.serializers import ProductSerializer


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
