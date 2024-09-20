from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from users_service.views import UserRegisterView, UserProfileView

app_name = "users_service"

routers = DefaultRouter()

urlpatterns = [
    path("", UserRegisterView.as_view()),
    path("me/", UserProfileView.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
