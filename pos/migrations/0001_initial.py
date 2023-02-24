# Generated by Django 4.1.7 on 2023-02-24 14:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=200)),
                ('category_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=200)),
                ('product_price', models.IntegerField()),
                ('product_fav', models.BooleanField(default=False)),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.category', verbose_name='Category')),
                ('product_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('table_id', models.AutoField(primary_key=True, serialize=False)),
                ('table_name', models.CharField(max_length=100)),
                ('table_status', models.BooleanField(default=False)),
                ('table_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('sale_id', models.AutoField(primary_key=True, serialize=False)),
                ('sale_date', models.CharField(max_length=50)),
                ('sale_bill', models.IntegerField()),
                ('sale_quantity', models.IntegerField()),
                ('sale_price', models.IntegerField()),
                ('sale_product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.product', verbose_name='Product')),
                ('sale_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('live', models.BooleanField(default=False)),
                ('counter_ip', models.CharField(max_length=200)),
                ('kitchen_ip', models.CharField(max_length=200)),
                ('mobile', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('business_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=150)),
                ('pro_usr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_product', models.IntegerField()),
                ('cart_quantity', models.IntegerField()),
                ('cart_direc', models.TextField(null=True)),
                ('cart_table_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.table', verbose_name='Table')),
                ('cart_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_number', models.IntegerField()),
                ('bill_date', models.CharField(max_length=100)),
                ('bill_data', models.TextField()),
                ('bill_total', models.IntegerField()),
                ('bill_payment_type', models.CharField(max_length=100)),
                ('bill_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
