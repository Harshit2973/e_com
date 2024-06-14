# cart/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from store.models import Product, Customer
from django.shortcuts import get_object_or_404

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        session_key = self.request.session.session_key
        customer = self.request.user if self.request.user.is_authenticated else None
        if customer:
            return Cart.objects.filter(customer=customer)
        else:
            return Cart.objects.filter(session_key=session_key)

    def create(self, request, *args, **kwargs):
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        customer = request.user if request.user.is_authenticated else None

        cart, created = Cart.objects.get_or_create(
            customer=customer, session_key=session_key
        )
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        cart_id = self.request.data.get('cart')
        cart = get_object_or_404(Cart, id=cart_id)
        serializer.save(cart=cart)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
