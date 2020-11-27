from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from .filters import OrderFilter
from .forms import OrderForm, OrderFormSet
from .models import Product, Order, Customer


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'order_list': orders,
               'customer_list': customers,
               'total_orders': total_orders,
               'total_customers': total_customers,
               'delivered': delivered,
               'pending': pending}
    return render(request, 'accounts/dashboard.html', context)


class ProductList(ListView):
    model = Product
    paginate_by = 5


class CustomerDetail(DetailView):
    model = Customer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_filter = OrderFilter(self.request.GET)
        context['order_filter'] = order_filter
        return context

    def get_queryset(self):

        return self.get_context_data()['order_filter'].qs


class CustomerCreate(CreateView):
    model = Customer
    success_url = reverse_lazy('accounts:home')


class CustomerUpdate(UpdateView):
    model = Customer
    success_url = reverse_lazy('accounts:home')


class CustomerDelete(DeleteView):
    model = Customer
    success_url = reverse_lazy('accounts:home')


def order_create(request, pk):
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)


class OrderUpdate(UpdateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('accounts:home')


class OrderDelete(DeleteView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('accounts:home')
