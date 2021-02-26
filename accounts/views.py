from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.views.generic.detail import SingleObjectMixin

from .decorators import *
from .filters import OrderFilter
from .forms import OrderForm, OrderFormSet, CreateUserForm, CustomerForm
from .models import Product, Order, Customer


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:home')
        else:
            messages.error(request, 'Username or Password is not correct')
    return render(request, 'accounts/login.html', context={})


def logout_user(request):
    logout(request)
    return redirect('accounts:login')


@method_decorator(unauthenticated_user, name='dispatch')
class Register(CreateView):
    model = User
    template_name = 'accounts/user_form.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('accounts:login')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('accounts:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        group = Group.objects.get(name='customer')
        user.groups.add(group)
        messages.success(self.request, 'Account was created for ' + username)
        return super().form_valid(form)


@login_required()
def home(request):
    orders = Order.objects.order_by('-date_created')
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    customers = Customer.objects.all()
    total_customers = customers.count()
    context = {'order_list': orders[:5],
               'customer_list': customers,
               'total_orders': total_orders,
               'total_customers': total_customers,
               'delivered': delivered,
               'pending': pending}
    return render(request, 'accounts/dashboard.html', context)


class ProductList(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 5
    queryset = model.objects.order_by('-date_created')


class CustomerCreate(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('accounts:home')


class CustomerUpdate(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('accounts:home')


class CustomerDelete(LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy('accounts:home')


class OrderCreate(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.customer = None

    def dispatch(self, request, *args, **kwargs):
        self.customer = Customer.objects.get(id=self.kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = OrderFormSet(instance=self.customer)
        return context

    def post(self, request, *args, **kwargs):
        formset = OrderFormSet(request.POST, instance=self.customer)
        if formset.is_valid():
            formset.save()
            return self.form_valid(formset)

    def get_success_url(self):
        return reverse_lazy('accounts:orders', kwargs={'pk': self.customer.id})


class CustomerDetail(LoginRequiredMixin, SingleObjectMixin, ListView):
    model = Customer
    queryset = model.objects.all()
    paginate_by = 5

    def __init__(self):
        super(CustomerDetail, self).__init__()
        self.object = None

    def get_queryset(self):
        self.object = self.get_object(queryset=self.queryset)
        return OrderFilter(self.request.GET,
                           queryset=self.object.order_set.order_by('-date_created')).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_filter'] = OrderFilter(self.request.GET)
        return context


class OrderUpdate(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('accounts:home')


class OrderDelete(LoginRequiredMixin, DeleteView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('accounts:home')
