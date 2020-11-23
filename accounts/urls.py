from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.ProductList.as_view(), name='products'),
    path('customer/<int:pk>/', views.CustomerDetail.as_view(), name='customer'),
    path('customer/update/<int:pk>/', views.CustomerUpdate.as_view(), name='customer_update'),
    path('customer/delete/<int:pk>/', views.CustomerDelete.as_view(), name='customer_delete'),
    path('order/create/', views.OrderCreate.as_view(), name='order_create'),
    path('order/update/<int:pk>/', views.OrderUpdate.as_view(), name='order_update'),
    path('order/delete/<int:pk>/', views.OrderDelete.as_view(), name='order_delete'),
]
