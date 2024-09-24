from django.urls import path
from users.views import MyTokenObtainPairView, RegisterView, ChangePasswordView, UpdateUserView
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from users import views as user_views

urlpatterns = [
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("register/", RegisterView.as_view(), name="auth_register"),
    path("change_password/<int:pk>/", ChangePasswordView.as_view(), name="auth_change_password"),
    path("update_profile/<int:pk>/", UpdateUserView.as_view(), name="auth_update_profile"),
    path("profile/", user_views.profile, name="profile"),
]
