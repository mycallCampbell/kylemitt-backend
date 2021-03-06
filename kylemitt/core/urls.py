from django.urls import path
from . import views

urlpatterns = [
    # path('users/login', views.MyTokenObtainPairView.as_view(),
    #      name='token_obtain_pair'),
    path('', views.getRoutes, name='routes'),
    # path('users/profile', views.getUserProfile, name='user-profile'),
    path('products-collection/', views.getProductsCollection,
         name='product-collection'),
    path('products-ring/', views.getProductsRing, name='products-ring'),
    path('products-bangle/', views.getProductsBangle, name='products-bangle'),
    path('products-necklace/', views.getProductsNecklace, name='product-necklace'),
    path('products-bracelet/', views.getProductsBracelet, name='product-bracelet'),
    path('products-earring/', views.getProductsEarring, name='product-earring'),
    path('products-chain/', views.getProductsChain, name='product-chain'),
    path('product/<str:pk>', views.getProduct, name='product'),
    path('client-secret/', views.getClientSecret, name='client-secret'),
    path('webhook/stripe', views.stripe_webhook, name='stripe-webhook'),
    path('addorder/', views.addOrderItems, name='add-order'),
    path('sendEmail/', views.sendEmail, name='send-email'),
    path('sendPurchaseEmail/', views.sendPurchaseEmail, name='purchaseEmail'),
    path('subscribe/', views.subscribe, name='subscribe'),
]
