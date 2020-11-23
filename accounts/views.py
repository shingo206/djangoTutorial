from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from .models import Product, Order, Customer
from .forms import OrderForm


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'order_list': orders, 'customer_list': customers, 'total_orders': total_orders,
               'total_customers': total_customers, 'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/dashboard.html', context)


class ProductList(ListView):
    model = Product


class CustomerDetail(DetailView):
    model = Customer


class CustomerCreate(CreateView):
    model = Customer
    success_url = reverse_lazy('accounts:home')


class CustomerUpdate(UpdateView):
    model = Customer
    success_url = reverse_lazy('accounts:home')


class CustomerDelete(DeleteView):
    model = Customer
    success_url = reverse_lazy('accounts:home')


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('accounts:home')


class OrderUpdate(UpdateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('accounts:home')


class OrderDelete(DeleteView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('accounts:home')
