from django.urls import path

from main.views import AddProductView, ProductAPIView, ProductDetailAPIView, ShoppingcartAPIView, \
    AddShoppingcartAPIView, GetSectionsAPIView, SectionsAPIView, CategoriesAPIView

urlpatterns = [
    path('add-product', AddProductView.as_view(), name='add-product'),
    path('product/<str:slug>', ProductDetailAPIView.as_view(), name='product-detail'),
    path('product', ProductAPIView.as_view(), name='product'),
    path('get-sections', GetSectionsAPIView.as_view(), name='get-sections'),
    path('section', SectionsAPIView.as_view(), name='section'),
    path('category', CategoriesAPIView.as_view(), name='category'),
    path('shopping-cart', ShoppingcartAPIView.as_view(), name='shopping-cart'),
    path('add-shopping', AddShoppingcartAPIView.as_view(), name='add-shopping')
]
