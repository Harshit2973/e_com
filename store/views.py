from rest_framework import viewsets, status # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.permissions import AllowAny, IsAuthenticated # type: ignore
from rest_framework.views import APIView # type: ignore
from .serializers import (
    SignUpSerializer,
    EmailLoginSerializer,
    CategorySerializer,
    CustomerSerializer,
    ProductSerializer,
    OrderSerializer,
    MessageSerializer
)
from .models import Category, Customer, Product, Order, Message
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token # type: ignore
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action # type: ignore

class CategoryViewSet(viewsets.ViewSet):
    serializer_class = CategorySerializer

    def list(self, request):
        category_name = request.query_params.get('name')

        if not category_name:
            return Response({"message": "Category name parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(name__iexact=category_name)
            products = Product.objects.filter(category=category)
            product_serializer = ProductSerializer(products, many=True)
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"message": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        category_name = self.request.query_params.get('category_name', None)
        if category_name:
            queryset = queryset.filter(category__name__iexact=category_name)
        return queryset
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
class ProductImageView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            image_url = product.image.url if product.image else None
            return Response({'image_url': image_url}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class SignupViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = EmailLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            logout(request)
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Message.objects.all()
        return Message.objects.filter(is_read_by_admin=False)

    def perform_create(self, serializer):
        serializer.save()
