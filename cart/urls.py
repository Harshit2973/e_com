from django.urls import path, include
from rest_framework.routers import DefaultRouter # type: ignore

router = DefaultRouter()
urlpatterns = [
    path('api/', include(router.urls)),
    
]
