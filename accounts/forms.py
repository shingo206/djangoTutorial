from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, inlineformset_factory

from accounts.models import Order, Customer


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


OrderFormSet = inlineformset_factory(
    parent_model=Customer,
    model=Order,
    form=OrderForm,
    can_delete=True,
    extra=10,
)
