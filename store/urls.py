from django.urls import path, include
from rest_framework.routers import DefaultRouter # type: ignore
from .views import CategoryViewSet, CustomerViewSet, ProductViewSet, OrderViewSet, SignupViewSet, LoginViewSet, LogoutViewSet,ProductImageView,MessageViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')  
router.register(r'customers', CustomerViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'signup', SignupViewSet, basename='signup')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'logout', LogoutViewSet, basename='logout')
router.register(r'messages', MessageViewSet)
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/product-image/<int:pk>/', ProductImageView.as_view(), name='product-image'),
    path('api/categories/<int:pk>/products/', CategoryViewSet.as_view({'get': 'products'}), name='category-products'),
]
