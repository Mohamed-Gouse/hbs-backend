from django.urls import path
from .views import RegisterView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', RegisterView.as_view()),
    path('signin/', LoginView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
]
