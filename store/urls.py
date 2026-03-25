from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('buyer-dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('vendor-dashboard/', views.vendor_dashboard, name='vendor_dashboard'),

    path('stores/', views.store_list, name='store_list'),
    path('stores/create/', views.store_create, name='create_store'),
    path('stores/<int:store_id>/', views.store_detail, name='store_detail'),

    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/create/', views.product_create, name='create_product'),

    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),

    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset/<str:token>/', views.reset_user_password, name='reset_user_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('reddit/', views.reddit_feed, name='reddit_feed'),

    # API ROUTES (PART 2 TASK)
    path('api/store/create/', views.api_create_store, name='api_create_store'),
    path('api/product/add/', views.api_add_product, name='api_add_product'),
    path('api/vendor/<int:vendor_id>/stores/', views.api_vendor_stores, name='api_vendor_stores'),
    path('api/store/<int:store_id>/products/', views.api_store_products, name='api_store_products'),
    path('api/products/<int:product_id>/reviews/', views.api_product_reviews, name='api_product_reviews'),

    # =========================
# DRF API URLs (PART 2)
# =========================
path('api/store/create/', views.api_create_store, name='api_create_store'),
path('api/product/add/', views.api_add_product, name='api_add_product'),
path('api/vendor/<int:vendor_id>/stores/', views.api_vendor_stores, name='api_vendor_stores'),
path('api/store/<int:store_id>/products/', views.api_store_products, name='api_store_products'),
path('api/product/<int:product_id>/reviews/', views.api_product_reviews, name='api_product_reviews'),
]