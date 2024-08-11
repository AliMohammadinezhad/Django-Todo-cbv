from django.urls import path
import rest_framework_simplejwt.views as auth_views

from . import views

urlpatterns = [
    # registration
    path("registration/", views.RegistrationView.as_view(), name="registration"),
    # activation
    path(
        "activation/confirm/<str:token>",
        views.ActivationApiView.as_view(),
        name="activation",
    ),
    # resend activation
    path(
        "activation/resend/",
        views.ActivationResendApiView.as_view(),
        name="activation-resend",
    ),
    # token login and logout
    path("token/login/", views.CustomObtainAuthToken.as_view(), name="token-login"),
    path("logout/", views.CustomDiscardAuthToken.as_view(), name="token-logout"),
    # password change
    path(
        "change-password/",
        views.ChangePasswordApiView.as_view(),
        name="change-password",
    ),
    # password reset
    path("reset-password/", views.ResetPasswordView.as_view(), name="reset-password"),
    path(
        "reset-password/confirm/<str:token>",
        views.ResetPasswordConfirmView.as_view(),
        name="reset-password-confirm",
    ),
    # login jwt
    path("jwt/create/", auth_views.TokenObtainPairView.as_view(), name="token-create"),
    path("jwt/refresh/", auth_views.TokenRefreshView.as_view(), name="token-refresh"),
    path("jwt/verify/", auth_views.TokenVerifyView.as_view(), name="token-verify"),
]
