from django.forms import ModelForm, inlineformset_factory

from accounts.models import Order, Customer


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


OrderFormSet = inlineformset_factory(
    parent_model=Customer,
    model=Order,
    form=OrderForm,
    can_delete=True,
    extra=10,
)
