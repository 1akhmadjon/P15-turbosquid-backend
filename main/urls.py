from django.urls import path

from main.views import AddProductView, ProductAPIView, ProductDetailAPIView, ShoppingcartAPIView, AddShoppingcartAPIView

urlpatterns = [
    path('add-product', AddProductView.as_view(), name='add-product'),
    path('product/<str:slug>', ProductDetailAPIView.as_view(), name='product-detail'),
    path('product', ProductAPIView.as_view(), name='product'),
    path('shopping-cart', ShoppingcartAPIView.as_view(), name='shopping-cart'),
    path('add-shopping', AddShoppingcartAPIView.as_view(), name='add-shopping')
]
