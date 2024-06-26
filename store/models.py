from django.db import models
import datetime


# Categories of Product
class Category(models.Model):
    name = models.CharField(max_length=100)
    try:
        def __str__(self):
            return self.name
        class Meta:
            verbose_name_plural='categories'
    except:
        Message.sucess() # type: ignore
class Customer(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=16)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=128)  # No write_only argument here

    def __str__(self):
        return f'{self.first_name} {self.last_name} '

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=255, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product')
    #Add sale
    is_sale=models.BooleanField(default=False)
    sale_price=models.DecimalField(default=0, decimal_places=2, max_digits=10)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=255, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.date.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'Order {self.id} for {self.product.name}'
class Message(models.Model):
    sender = models.CharField(max_length=100)
    message = models.TextField()
    is_read_by_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.message}"
    