# store/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from django.contrib.auth import authenticate, login, logout
from .models import Category, Customer, Product, Order, Message
from .serializers import CategorySerializer, CustomerSerializer, ProductSerializer, OrderSerializer, SignUpSerializer, LoginSerializer, MessageSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class SignUpViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = SignUpSerializer

class LoginViewSet(viewsets.ViewSet):
    def create(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        customer = authenticate(username=email, password=password)

        if customer is not None:
            login(request, customer)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutViewSet(viewsets.ViewSet):
    def list(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

class ProductImageView(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductImageSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class SessionKeyViewSet(APIView):
    def get(self, request, *args, **kwargs):
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        return Response({"session_key": session_key}, status=status.HTTP_200_OK)
