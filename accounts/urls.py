from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/<uid64>/<token>', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('register/', views.Register.as_view(), name='register'),
    path('products/', views.ProductList.as_view(), name='products'),
    path('customer/create/', views.CustomerCreate.as_view(), name='customer_create'),
    path('customer/update/<int:pk>/', views.CustomerUpdate.as_view(), name='customer_update'),
    path('customer/delete/<int:pk>/', views.CustomerDelete.as_view(), name='customer_delete'),
    path('orders/<int:pk>/', views.CustomerDetail.as_view(), name='orders'),
    path('order/create/<int:pk>/', views.OrderCreate.as_view(), name='order_create'),
    path('order/update/<int:pk>/', views.OrderUpdate.as_view(), name='order_update'),
    path('order/delete/<int:pk>/', views.OrderDelete.as_view(), name='order_delete'),
]
