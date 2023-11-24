import datetime

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination

from .models import Products, Shoppingcart, Subscription
from .documents import DocumentProduct
from .serializers import (
    ProductSerializer,
    ShoppingcartSerializers, EmailSerializer,
    ProductDocumentSerializer
)


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
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.user.id
        shoppingcart = Shoppingcart.objects.filter(user_id_id=user_id)
        shoppingcart_serializers = ShoppingcartSerializers(shoppingcart, many=True)
        return Response(shoppingcart_serializers.data)


class AddShoppingcartAPIView(APIView):
    permission_classes = (IsAuthenticated,)

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
            return Response(shoppingcart_serializers.data)


class ProductUpdateAPIView(GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request, pk):
        product = Products.objects.get(pk=pk)
        product_serializer = ProductSerializer(product)
        return Response(product_serializer.data)

    def put(self, request, pk):
        title = request.POST.get('title')
        description = request.POST.get('description')
        product = Products.objects.get(pk=pk)
        product.title = title
        product.description = description
        product.expires_at = datetime.datetime.now()
        product.save()
        product_serializer = ProductSerializer(product)
        return Response(product_serializer.data)

    def patch(self, request, pk):
        title = request.POST.get('title', None)
        description = request.POST.get('description', None)
        product = Products.objects.get(pk=pk)
        if title:
            product.title = title
        if description:
            product.description = description
        product.save()
        product_serializer = ProductSerializer(product)
        return Response(product_serializer.data)

    def delete(self, request, pk):
        Products.objects.get(pk=pk).delete()
        return Response(status=204)


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductSearchViewSet(DocumentViewSet):
    document = DocumentProduct
    serializer_class = ProductDocumentSerializer
    pagination_class = CustomPageNumberPagination

    filter_backends = [
        FilteringFilterBackend,
        SearchFilterBackend,
        SuggesterFilterBackend,
    ]

    search_fields = (
        'title',
        'slug',
        'description',
        'price',
    )

    filter_fields = {
        'title': 'title',
        'slug': 'slug',
        'description': 'description',
        'price': 'price',
    }

    suggester_fields = {
        'title': {
            'field': 'title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'slug': {
            'field': 'slug.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        }
    }

    def list(self, request, *args, **kwargs):
        search_term = self.request.query_params.get('search', '')
        query = Q('multi_match', query=search_term, fields=self.search_fields)
        queryset = self.filter_queryset(self.get_queryset().query(query))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SubscribeAPIView(GenericAPIView):
    serializer_class = EmailSerializer
    permission_classes = ()

    def post(self, request):
        if not Subscription.objects.filter(email=request.data['email']).exists():
            email_serializer = self.serializer_class(data=request.data)
            email_serializer.is_valid(raise_exception=True)
            email_serializer.save()
        else:
            return Response({'success': False, 'message': 'Already subscribed!'}, status=400)
        return Response({'success': True, 'message': 'Successfully subscribed :)'})
