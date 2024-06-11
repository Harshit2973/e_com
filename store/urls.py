from django.urls import path, include
from rest_framework.routers import DefaultRouter # type: ignore
from .views import CategoryViewSet, CustomerViewSet, ProductViewSet, OrderViewSet, SignupViewSet, LoginViewSet, LogoutViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'signup', SignupViewSet, basename='signup')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'logout', LogoutViewSet, basename='logout')

urlpatterns = [
    path('api/', include(router.urls)),
]
