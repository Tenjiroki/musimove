from django.urls import path
from . import views

urlpatterns = [
    path('', views.base_view, name='base_generic'),  
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('user-list/', views.user_list, name='user_list'),
    path('offers/', views.user_offers, name='offers'),
    path('offers/book/<int:offer_id>/', views.book_offer, name='book_offer'),
    path('instrument/<int:instrument_id>/', views.instrument_detail, name='instrument_detail'),
    path('brand/<int:brand_id>/', views.brand_detail, name='brand_detail'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('user/orders/', views.user_orders, name='user_orders'),
    path('order/<int:order_id>/delivery/', views.delivery_detail, name='delivery_detail'),
    path('order/<int:order_id>/review/', views.review_detail, name='review_detail'),
    path('order/<int:order_id>/payment/', views.payment_detail, name='payment_detail'),
    path('wishlist/', views.user_wishlist, name='user_wishlist'),
    path('notifications/', views.user_notifications, name='user_notifications'),
    path('homepage/', views.homepage_view, name='homepage'),
    path('create_offer/', views.create_offer, name='create_offer'),
    path('offer_success/', views.offer_success, name='offer_success'),
    ]
