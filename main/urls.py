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
    CategoriesAPIView,
    ProductSingleAPIView,
    CheckoutShoppingcart,
    OrderAPIView, ProductsFilterView,
    LikeUserAPIView, LikeDetailUserAPIView,
    CommentUserAPIView
)

router = routers.DefaultRouter(trailing_slash=False)
router.register('product-search', ProductSearchViewSet, basename='search_todo')  # done

urlpatterns = [
    path('add-product', AddProductView.as_view(), name='add-product'),  # done
    path('product/<str:slug>', ProductDetailAPIView.as_view(), name='product-detail'),  # done
    path('product', ProductAPIView.as_view(), name='product'),  # done
    path('get-sections', GetSectionsAPIView.as_view(), name='get-sections'),  # done
    path('section', SectionsAPIView.as_view(), name='section'),  # done
    path('category', CategoriesAPIView.as_view(), name='category'),  # done
    path('shopping-cart', ShoppingcartAPIView.as_view(), name='shopping-cart'),  # done
    path('add-shopping', AddShoppingcartAPIView.as_view(), name='add-shopping'),  # done
    path('product-update/<int:product_id>', ProductUpdateAPIView.as_view(), name='product_update'),  # done
    path('subscribe', SubscribeAPIView.as_view(), name='subscribe'),  # done
    path('product-single/<int:product_id>', ProductSingleAPIView.as_view(), name='product_single'),  # done
    path('checkout-shoppingcart/<int:product_id>', CheckoutShoppingcart.as_view(), name='checkout-shoppingcart'),
    # done
    path('order', OrderAPIView.as_view(), name='order'),  # done
    path('', include(router.urls)),  # done
    path('filter', ProductsFilterView.as_view(), name='filter'),  # done
    path('like/<int:product_id>', LikeUserAPIView.as_view(), name='like'),  # done
    path('like-detail', LikeDetailUserAPIView.as_view(), name='like-detail'),  # done
    path('comment/<int:product_id>', CommentUserAPIView.as_view(), name='comment'),  # done
]
