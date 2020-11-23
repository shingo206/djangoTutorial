from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from accounts.models import Product, Order, Customer


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


class CustomerUpdate(UpdateView):
    model = Customer


class CustomerDelete(DeleteView):
    model = Customer
