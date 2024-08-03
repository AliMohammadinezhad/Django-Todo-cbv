from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from mail_templated import EmailMessage
import jwt

from ..utils.threading import EmailThread
from .serializers import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    ChangePasswordSerializer,
    ActivationResendSerializer,
    ResetPasswordSerializer,
    ChangePasswordConfirmSerializer,
)

User = get_user_model()


class RegistrationView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            data = {
                "details": [
                    f"user {serializer.validated_data.get("username")} with email {email} created succefully. verfiy your email.",
                ],
            }
            serializer.save()
            user_obj = get_object_or_404(User, email=email)
            token = self.get_token_for_user(user_obj)
            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "admin@admin.com",
                to=[email],
            )
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    
class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        data = {"user_id": user.pk, "username": user.username, "email": user.email ,"token": token.key}
        return Response(data, status=status.HTTP_201_CREATED)


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Token.DoesNotExist as e:
            return Response(
                {"details": "you are not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class ChangePasswordApiView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    model = User

    def get_object(self):
        user = self.request.user
        return user

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get('current_password')):
                return Response(
                    {"old_password": ["Wrong password"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.set_password(serializer.data.get('new_password1'))
            user.save()
            return Response(
                {"details": "password changed successefully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
class ActivationApiView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = token.get('user_id')
        except jwt.exceptions.ExpiredSignatureError:
            return Response({"details":"token has been expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.InvalidSignatureError:
            return Response({"details":"token is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_obj = get_object_or_404(User, pk=user_id)
        if user_obj.is_active:
            return Response({"details":"your account has already been activated"})
        user_obj.is_active = True
        user_obj.save()
        return Response({"details": "your account has been verified and activated successfully"})


class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = ActivationResendSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            data = {
                "details": 
                    f"activation email sent to email: {email}"
                
            }
            user_obj = serializer.validated_data.get('user')
            token = self.get_token_for_user(user_obj)
            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "admin@admin.com",
                to=[email],
            )
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    
    def post(self, request,*args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        data = {
            "details": 
                f"Reset email sent to: {email}"
            
        }
        user_obj = serializer.validated_data.get('user')
        token = self.get_token_for_user(user_obj)
        email_obj = EmailMessage(
            "email/reset_email.tpl",
            {"token": token},
            "admin@admin.com",
            to=[email],
        )
        EmailThread(email_obj).start()
        return Response(data, status=status.HTTP_200_OK)
    
    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

class ResetPasswordConfirmView(generics.GenericAPIView):
    serializer_class = ChangePasswordConfirmSerializer
    
    def post(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = token.get('user_id')
        except jwt.exceptions.ExpiredSignatureError:
            return Response({"details":"token has been expired"}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.InvalidSignatureError:
            return Response({"details":"token is not valid"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['new_password1']
        user_obj = get_object_or_404(User, pk=user_id)
        user_obj.set_password(password)
        user_obj.save()
        return Response({"details": "password changed succefully."})