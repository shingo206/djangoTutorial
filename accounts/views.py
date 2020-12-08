from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.views.generic.detail import SingleObjectMixin

from .decorators import unauthenticated_user, allowed_users
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
            messages.info(request, 'Username or Password is not correct')
    return render(request, 'accounts/login.html', context={})


def logout_user(request):
    logout(request)
    return redirect('accounts:login')


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
        user = form.cleaned_data.get('username')
        messages.success(self.request, 'Account was created for ' + user)
        return super().form_valid(form)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin', 'customer'])
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
    login_url = 'accounts:login'
    queryset = Product.objects.order_by('-date_created')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CustomerCreate(LoginRequiredMixin, CreateView):
    model = Customer
    login_url = 'accounts:login'
    success_url = reverse_lazy('accounts:home')

    @allowed_users(allowed_roles=['admin'])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CustomerUpdate(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    login_url = 'accounts:login'
    success_url = reverse_lazy('accounts:home')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CustomerDelete(LoginRequiredMixin, DeleteView):
    model = Customer
    login_url = 'accounts:login'
    success_url = reverse_lazy('accounts:home')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


#
#
# @login_required(login_url='accounts:login')
# @allowed_users(allowed_roles=['admin', 'customer'])
# def order_create(request, pk):
#     customer = Customer.objects.get(id=pk)
#     formset = OrderFormSet(instance=customer)
#     if request.method == 'POST':
#         formset = OrderFormSet(request.POST, instance=customer)
#         if formset.is_valid():
#             formset.save()
#             return redirect('/')
#     context = {'formset': formset}
#     return render(request, 'accounts/order_form.html', context)


class OrderCreate(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    login_url = 'accounts:login'
    success_url = reverse_lazy('accounts:home')

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
            return redirect('accounts:orders', **kwargs)


class OrderList(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 5
    login_url = 'accounts:login'

    def __init__(self):
        super(OrderList, self).__init__()
        self.customer = None

    def get_queryset(self):
        self.customer = Customer.objects.get(id=self.kwargs.get('pk'))
        return OrderFilter(self.request.GET,
                           queryset=Order.objects.filter(customer=self.customer).order_by('-date_created')).qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = self.customer
        context['order_filter'] = OrderFilter(self.request.GET)
        return context


class CustomerDetail(LoginRequiredMixin, SingleObjectMixin, ListView):
    model = Customer
    paginate_by = 5
    login_url = 'accounts:login'

    def __init__(self):
        super(CustomerDetail, self).__init__()
        self.object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.model.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return OrderFilter(self.request.GET,
                           queryset=self.object.order_set.order_by('-date_created')).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customer'] = self.object
        context['order_filter'] = OrderFilter(self.request.GET)
        return context


class OrderUpdate(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    login_url = 'accounts:login'
    success_url = reverse_lazy('accounts:home')


class OrderDelete(LoginRequiredMixin, DeleteView):
    model = Order
    form_class = OrderForm
    login_url = 'accounts:login'
    success_url = reverse_lazy('accounts:home')
