from django.urls import path, include
from rest_framework import routers

<<<<<<< Updated upstream
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
    CategoriesAPIView,
    ProductSingleAPIView,
    CheckoutShoppingcart,
    OrderAPIView
)

router = routers.DefaultRouter(trailing_slash=False)
router.register('product-search', ProductSearchViewSet, basename='search_todo')
=======
from main.views import AddProductView, ProductAPIView, ProductDetailAPIView, ShoppingcartAPIView, \
    AddShoppingcartAPIView, ProductUpdateAPIView, ProductsFilterView, LikeUserAPIView, \
    LikeDetailUserAPIView, CommentUserAPIView
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
    path('subscribe', SubscribeAPIView.as_view(), name='subscribe'),
    path('product-single/<int:pk>', ProductSingleAPIView.as_view(), name='product_single'),
    path('checkout-shoppingcart/<int:product_id>', CheckoutShoppingcart.as_view(), name='checkout-shoppingcart'),
    path('order', OrderAPIView.as_view(), name='order'),
    path('', include(router.urls)),
=======
    path('filter', ProductsFilterView.as_view(), name='filter'),
    path('like/<int:pk>', LikeUserAPIView.as_view(), name='like'),
    path('like-detail', LikeDetailUserAPIView.as_view(), name='like-detail'),
    path('comment/<int:pk>', CommentUserAPIView.as_view(), name='comment'),
>>>>>>> Stashed changes
]
