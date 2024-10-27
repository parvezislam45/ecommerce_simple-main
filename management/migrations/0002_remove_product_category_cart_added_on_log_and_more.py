# Generated by Django 5.1.1 on 2024-09-30 10:27

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.AddField(
            model_name='cart',
            name='added_on',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 9, 30, 10, 27, 22, 201241, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('log', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(default='login', max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loguser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
