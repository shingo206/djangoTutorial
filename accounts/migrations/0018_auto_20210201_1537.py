# Generated by Django 3.1.5 on 2021-02-01 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20210201_1530'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'permissions': [('create_customers', 'allow to create new customer'), ('update_customers', 'allow to update customer'), ('delete_customers', 'allow to delete customer')]},
        ),
    ]