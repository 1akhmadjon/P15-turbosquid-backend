from django.urls import path, include
from rest_framework import routers

from main.views import (
    AddProductView,
    ProductAPIView,
    ProductDetailAPIView,
    ShoppingcartAPIView,
    AddShoppingcartAPIView,
    ProductUpdateAPIView,
    SubscribeAPIView,
    ProductSearchViewSet,
    GetSectionsAPIView,
    SectionsAPIView,
    CategoriesAPIView
)

router = routers.DefaultRouter(trailing_slash=False)
router.register('product-search', ProductSearchViewSet, basename='search_todo')

urlpatterns = [
    path('add-product', AddProductView.as_view(), name='add-product'),
    path('product/<str:slug>', ProductDetailAPIView.as_view(), name='product-detail'),
    path('product', ProductAPIView.as_view(), name='product'),
    path('get-sections', GetSectionsAPIView.as_view(), name='get-sections'),
    path('section', SectionsAPIView.as_view(), name='section'),
    path('category', CategoriesAPIView.as_view(), name='category'),
    path('shopping-cart', ShoppingcartAPIView.as_view(), name='shopping-cart'),
    path('add-shopping', AddShoppingcartAPIView.as_view(), name='add-shopping'),
    path('product-update/<int:pk>', ProductUpdateAPIView.as_view(), name='product_update'),
    path('subscribe', SubscribeAPIView.as_view(), name='subscribe'),
    path('', include(router.urls))
]
