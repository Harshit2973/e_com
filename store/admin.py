from django.contrib import admin
from .models import Category, Customer, Product, Order, Message

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    search_fields = ('name',)
    list_filter = ('category',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'quantity', 'date', 'status')
    search_fields = ('customer__first_name', 'customer__last_name', 'product__name')
    list_filter = ('status', 'date')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'message', 'is_read_by_admin', 'created_at')  
    list_filter = ('is_read_by_admin',)
    search_fields = ('sender', 'message')