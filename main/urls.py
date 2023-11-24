from django.urls import path, include
from rest_framework import routers

from main.views import (
    AddProductView,
    ProductAPIView,
    ProductDetailAPIView,
    ShoppingcartAPIView,
    AddShoppingcartAPIView,
    ProductSearchViewSet, EmailSubscriberAPIView, ProductUpdateAPIView
)

router = routers.DefaultRouter(trailing_slash=False)
router.register('product-search', ProductSearchViewSet, basename='search_product')

urlpatterns = [
    path('add-product', AddProductView.as_view(), name='add-product'),
    path('product/<str:slug>', ProductDetailAPIView.as_view(), name='product-detail'),
    path('product', ProductAPIView.as_view(), name='product'),
    path('shopping-cart', ShoppingcartAPIView.as_view(), name='shopping-cart'),
    path('product-update/<int:pk>', ProductUpdateAPIView.as_view(), name='product_update'),
    path('add-shopping', AddShoppingcartAPIView.as_view(), name='add-shopping'),
    path('subscribe', EmailSubscriberAPIView.as_view(), name='subscribe'),
    path('', include(router.urls))
]
