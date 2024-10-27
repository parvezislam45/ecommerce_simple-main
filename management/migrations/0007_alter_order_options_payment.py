# Generated by Django 5.1.1 on 2024-10-04 12:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_order_created_by_order_created_on_order_order_id_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-id']},
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('credit_debit_card', 'Credit/Debit Card'), ('paypal', 'PayPal')], max_length=20)),
                ('card_number', models.CharField(blank=True, max_length=16, null=True)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('security_code', models.CharField(blank=True, max_length=4, null=True)),
                ('cardholder_name', models.CharField(blank=True, max_length=100, null=True)),
                ('paypal_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('paypal_password', models.CharField(blank=True, max_length=100, null=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order_payment', to='management.order')),
            ],
        ),
    ]
