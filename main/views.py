import datetime

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination

from .documents import DocumentProduct

from drf_yasg.utils import swagger_auto_schema

from main.models import Products, Shoppingcart, Sections, Category, Subscription
from .serializers import ProductSerializer, ShoppingcartSerializers, CategorySerializer, QuerySerializer, EmailSerializer, ProductDocumentSerializer, \
    SectionSerializer
from django.contrib.auth.views import get_user_model

from main.models import Products, Shoppingcart, Order, UserBalance, Image, ArchiveShoppingcart
from .serializers import ProductSerializer, ShoppingcartSerializers
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from main.models import Products, Shoppingcart, Comment, Like
from .product_filters import ProductsFilter
from .serializers import ProductSerializer, ShoppingcartSerializers, CommentSerializer, LikeSerializer
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework import generics, status

User = get_user_model()

class ProductAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = ProductSerializer

    def get(self, request):
        product = Products.objects.all()
        product_data = ProductSerializer(product, many=True)
        return Response(product_data.data)


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
            product = Products.objects.get(slug=slug)
        except Products.DoesNotExist:
            return Response({'success': False}, status=404)
        product_serializer = ProductSerializer(product)
        return Response(product_serializer.data)



class ShoppingcartAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.user.id
        shoppingcart = Shoppingcart.objects.filter(user_id=user_id)
        shoppingcart_serializers = ShoppingcartSerializers(shoppingcart, many=True)
        return Response(shoppingcart_serializers.data)


class AddShoppingcartAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_id = request.user.id
        product_id = request.POST.get('product_id')
        if Shoppingcart.objects.filter(Q(user_id=user_id) & Q(product_id=product_id)).exists():
            shoppingcart = Shoppingcart.objects.get(Q(user_id=user_id) & Q(product_id=product_id))
            shoppingcart_serializers = ShoppingcartSerializers(shoppingcart)
            return Response(shoppingcart_serializers.data)
        else:
            shoppingcart = Shoppingcart.objects.create(
                product_id=product_id,
                user_id=user_id
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


class GetSectionsAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = SectionSerializer

    def get(self, request):
        sections = Sections.objects.all()
        sections_serializer = SectionSerializer(sections, many=True)
        return Response(sections_serializer.data)
class CheckoutShoppingcart(APIView):
    permission_classes = (IsAuthenticated, )

    def delete(self, request, product_id):
        user_id = request.user.id
        if not Shoppingcart.objects.filter(Q(user_id=user_id) & Q(product_id=product_id)).exists():
            return Response({'success': False, 'error': 'This user has no products with this id in their shopping cart'}, status=404)
        else:
            Shoppingcart.objects.get(Q(user_id=user_id) & Q(product_id=product_id)).delete()
            return Response({'success': True}, status=204)


class OrderAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        user = request.user.id
        total_price = 0
        user_shoppingcart = Shoppingcart.objects.filter(user_id=user)
        products = []
        for i in user_shoppingcart.values():
            product_id = i['product_id']
            product = Products.objects.filter(id=product_id)
            products += product.values()
        for i in products:
            total_price += i['price']

        user_wallet = UserBalance.objects.filter(user=user)
        user_wallet=user_wallet[0]
        user_balance = user_wallet.balance
        if total_price > user_balance:
            return Response({'success': False, 'error': 'Not enough money'})
        else:
            for i in user_shoppingcart:
                order = Order.objects.create(
                    user=request.user,
                    product=i.product,
                )
                order.save()
                product_id=i.product_id
                Shoppingcart.objects.get(product=product_id).delete()
                archiveshoppingcart = ArchiveShoppingcart.objects.create(
                    product=product_id,
                    user=user
                )
                archiveshoppingcart.save()
                user_balance = int(user_balance) - int(total_price)
                user_wallet.balance = user_balance
                user_wallet.save()


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


class ProductsFilterView(ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = ()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductsFilter

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


class LikeUserAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer

    def post(self, request, pk):
        product = Products.objects.get(pk=pk)
        if not Like.objects.filter(Q(user_id=request.user) & Q(product_id=pk)).exists():
            like = Like.objects.create(
                user=request.user, product=product,
            )
            like.save()
            like_serializer = LikeSerializer(like)
            return Response(like_serializer.data)
        return Response({'success': False}, status=401)


class LikeDetailUserAPIView(GenericAPIView):
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        liked_data = Like.objects.filter(user_id=request.user.id)
        if liked_data:
            like_serializer = LikeSerializer(liked_data)
            return Response(like_serializer.data)
        return Response({'success': False, 'message': "You don't have any liked products"})


class CommentUserAPIView(GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        product = Products.objects.get(pk=pk)
        message = request.data.get('message')
        if not Comment.objects.filter(Q(user_id=request.user.id) & Q(product_id=pk)).exists():
            comment = Comment.objects.create(
                user=request.user, message=message,
                product_id=product.id
            )
            comment.save()
            comment_serializer = CommentSerializer(comment)
            return Response(comment_serializer.data)
        return Response({'success': False}, status=401)
