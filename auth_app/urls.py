from django.urls import path
from .views import RegisterView, LoginView, verify_account
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', RegisterView.as_view()),
    path('signin/', LoginView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path('verify/<str:uidb64>/<str:token>/', verify_account, name='verify_account'),
]
