from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema

from main.models import Products, Shoppingcart, Sections, Category
from .serializers import ProductSerializer, ShoppingcartSerializers, CategorySerializer, QuerySerializer, \
    SectionSerializer


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


class GetSectionsAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = SectionSerializer

    def get(self, request):
        sections = Sections.objects.all()
        sections_serializer = SectionSerializer(sections, many=True)
        return Response(sections_serializer.data)


class SectionsAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = CategorySerializer

    @swagger_auto_schema(query_serializer=QuerySerializer)
    def get(self, request):
        query = request.GET.get('query')
        sections = Sections.objects.filter(Q(name=query) & Q(parent=None))
        categories = Category.objects.filter(section__in=sections)
        section_serializer = SectionSerializer(categories, many=True)
        return Response(section_serializer.data)


class CategoriesAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = CategorySerializer

    @swagger_auto_schema(query_serializer=QuerySerializer)
    def get(self, request):
        query = request.GET.get('query')
        categories = Category.objects.filter(Q(name=query) & Q(parent=None))
        products = Products.objects.filter(category__in=categories)
        product_serializer = ProductSerializer(products, many=True)
        return Response(product_serializer.data)


class ProductSingleAPIView(GenericAPIView):
    permission_classes = ()

    def get(self, request, pk):
        product = Products.objects.filter(pk=pk).first()
        sections = {
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'price': product.price,
            'category': product.category.name,
            'section': product.category.section.name
        }
        return Response(sections)
