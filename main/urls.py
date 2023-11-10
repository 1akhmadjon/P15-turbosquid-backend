from django.urls import path

from main.views import AddProductView, ProductAPIView, ProductDetailAPIView

urlpatterns = [
    path('add-product', AddProductView.as_view(), name='add-product'),
    path('product/<str:slug>', ProductDetailAPIView.as_view(), name='product-detail'),
    path('product', ProductAPIView.as_view(), name='product'),
]
