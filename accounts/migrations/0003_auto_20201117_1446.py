# Generated by Django 3.1.3 on 2020-11-17 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_order_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ManyToManyField(to='accounts.Customer'),
        ),
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.product'),
            preserve_default=False,
        ),
    ]
