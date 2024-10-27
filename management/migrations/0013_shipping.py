# Generated by Django 5.1.1 on 2024-10-09 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0012_alter_payment_expiration_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_fee', models.DecimalField(decimal_places=2, default=100.0, max_digits=10)),
            ],
        ),
    ]