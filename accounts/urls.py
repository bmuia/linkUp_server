from django.urls import path
from .views import RegistrationView, GetCurrentProfile, LogoutView, UpdateUserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('v1/register/', RegistrationView.as_view(), name='register-user'),
    path('v1/whoami/', GetCurrentProfile.as_view(), name='get-current-user'),
    path('v1/logout/', LogoutView.as_view(), name='logout-user'),

    path('v1/login/', TokenObtainPairView.as_view(), name='login-user'),
    path('v1/login/refresh/', TokenRefreshView.as_view(), name='refresh-tokens'),

    path('v1/user/update/',UpdateUserProfileView.as_view(), name='update-user-profile'),
]
