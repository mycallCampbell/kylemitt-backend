from django.urls import path
from . import views

urlpatterns = [
    # path('users/login', views.MyTokenObtainPairView.as_view(),
    #      name='token_obtain_pair'),
    path('', views.getRoutes, name='routes'),
    # path('users/profile', views.getUserProfile, name='user-profile'),
    path('products-ring/', views.getProductsRing, name='products-ring'),
    path('products-bangle/', views.getProductsBangle, name='products-bangle'),
    path('product-necklace/', views.getProductsNecklace, name='product-necklace'),
    path('product-bracelet/', views.getProductsBracelet, name='product-bracelet'),
    path('product-earring/', views.getProductsEarring, name='product-earring'),
    path('product-chain/', views.getProductsChain, name='product-chain'),
    path('product/<str:pk>', views.getProduct, name='product'),
    path('client-secret/', views.getClientSecret, name='client-secret'),
    path('webhook/stripe', views.stripe_webhook, name='stripe-webhook'),
    path('addorder/', views.addOrderItems, name='add-order'),
]
