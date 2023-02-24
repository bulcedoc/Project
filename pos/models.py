from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    pro_usr = models.ForeignKey(User,verbose_name="User", on_delete=models.CASCADE)
    live = models.BooleanField(default=False)
    counter_ip = models.CharField(max_length=200)
    kitchen_ip = models.CharField(max_length=200)
    mobile = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    business_name = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    def __str__(self):
        return self.mobile

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=200)
    category_user = models.ForeignKey(User,verbose_name="User", on_delete=models.CASCADE)
    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200)
    product_price = models.IntegerField()
    product_fav = models.BooleanField(default=False)
    product_category = models.ForeignKey(Category,verbose_name="Category", on_delete=models.CASCADE)
    product_user = models.ForeignKey(User,verbose_name="User", on_delete=models.CASCADE)
    def __str__(self):
        return self.product_name

class Bill(models.Model):
    bill_number = models.IntegerField()
    bill_user = models.ForeignKey(User,verbose_name="User", on_delete=models.CASCADE)
    bill_date = models.CharField(max_length=100)
    bill_data = models.TextField()
    bill_total = models.IntegerField()
    bill_payment_type = models.CharField(max_length=100)
    def __str__(self):
        return self.bill_number

class Table(models.Model):
    table_id = models.AutoField(primary_key=True)
    table_user = models.ForeignKey(User,verbose_name="User", on_delete=models.CASCADE)
    table_name = models.CharField(max_length=100)
    table_status = models.BooleanField(default=False)
    def __str__(self):
        return self.table_id

class Cart(models.Model):
    cart_table_id = models.ForeignKey(Table,verbose_name="Table", on_delete=models.CASCADE)
    cart_user = models.ForeignKey(User,verbose_name="User", on_delete=models.CASCADE)
    cart_product = models.IntegerField()
    cart_quantity = models.IntegerField()
    cart_direc = models.TextField(null=True)
    def __str__(self):
        return self.cart_table_id

class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True)
    sale_product_id = models.ForeignKey(Product,verbose_name="Product", on_delete=models.CASCADE)
    sale_user = models.ForeignKey(User,verbose_name="User", on_delete=models.CASCADE)
    sale_date = models.CharField(max_length=50)
    sale_bill = models.IntegerField()
    sale_product_name = models.CharField(max_length=100)
    sale_quantity = models.IntegerField()
    sale_price = models.IntegerField()
    def __str__(self):
        return self.sale_user