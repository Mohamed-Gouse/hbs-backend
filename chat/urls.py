from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessagedUsers

router = DefaultRouter()
router.register(r'messaged-users', MessagedUsers, basename='messaged-users')

urlpatterns = [
    path('', include(router.urls)),
]
