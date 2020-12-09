from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('products/', views.ProductList.as_view(), name='products'),
    path('customer/create/', views.CustomerCreate.as_view(), name='customer_create'),
    path('customer/update/<int:pk>/', views.CustomerUpdate.as_view(), name='customer_update'),
    path('customer/delete/<int:pk>/', views.CustomerDelete.as_view(), name='customer_delete'),
    path('orders/<int:pk>/', views.CustomerDetail.as_view(), name='orders'),
    # path('orders/<int:pk>/', views.OrderList.as_view(), name='orders'),
    path('order/create/<int:pk>/', views.OrderCreate.as_view(), name='order_create'),
    path('order/update/<int:pk>/', views.OrderUpdate.as_view(), name='order_update'),
    path('order/delete/<int:pk>/', views.OrderDelete.as_view(), name='order_delete'),
]
