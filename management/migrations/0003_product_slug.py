# Generated by Django 5.1.1 on 2024-09-30 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_remove_product_category_cart_added_on_log_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
