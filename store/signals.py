from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db import connection
from .models import Category, Product

def reset_sequence(table_name, pk_field):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT setval(pg_get_serial_sequence('{table_name}', '{pk_field}'), COALESCE(MAX({pk_field}), 1), false) FROM {table_name}")

@receiver(post_delete, sender=Category)
def reset_category_pk_sequence(sender, instance, **kwargs):
    reset_sequence('yourapp_category', 'id')

@receiver(post_delete, sender=Product)
def reset_product_pk_sequence(sender, instance, **kwargs):
    reset_sequence('yourapp_product', 'id')
