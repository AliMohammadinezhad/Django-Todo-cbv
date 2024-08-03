from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core import exceptions 
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=512)
    
    class Meta:
        model = User
        fields = ("username","email", "password", "password1")
        
    def validate(self, attrs):
        password1 = attrs.get("password1")
        password = attrs.get("password")
        
        
        if password1 != password:
            raise serializers.ValidationError({"details":"passwords do not match"})
        

        
        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
                
        return super().validate(attrs)
        
        
    def create(self, validated_data):
        validated_data.pop('password1', None)
        return User.objects.create_user(**validated_data)

class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("username"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )
    email = serializers.EmailField(
        label=_("Email"),
        write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        email = attrs.get('email')
        
        if username and password and email:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password, email=email)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            if not user.is_active:
                raise serializers.ValidationError({'details': 'user is not activated'})
            
        else:
            msg = _('Must include "username" and "password" and "email".')
            raise serializers.ValidationError(msg, code='authorization')

        
        attrs['user'] = user
        return attrs
 

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data =  super().validate(attrs)
        if not self.user.is_active:
                raise serializers.ValidationError({'details': 'user is not activated'})
        validated_data["username"] = self.user.username
        validated_data["user_id"] = self.user.id
        return validated_data 

class ChangePasswordSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True, source='password')
        
    def validate(self, attrs):
        new_password1 = attrs.get("new_password1")
        new_password2 = attrs.get("new_password2")
        
        
        if new_password1 != new_password2:
            raise serializers.ValidationError({"details":"passwords do not match"})
        
        try:
            validate_password(new_password1)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
                
        return super().validate(attrs)
        
class ActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    
    def validate(self, attrs):
        email = attrs.get("email")
        
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"details":"User does not exist"})
        if user_obj.is_active:
            raise serializers.ValidationError({"details":"user has been already activated and verified"})
        attrs['user'] = user_obj
        return super().validate(attrs) 
    
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    
    def validate(self, attrs):
        email = attrs.get("email")
        
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"details":"User does not exist."})
        if not user_obj.is_active:
            raise serializers.ValidationError({"details":"User is not activated."})
        attrs['user'] = user_obj
        return super().validate(attrs)

class ChangePasswordConfirmSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)
        
    def validate(self, attrs):
        new_password1 = attrs.get("new_password1")
        new_password2 = attrs.get("new_password2")
        
        
        if new_password1 != new_password2:
            raise serializers.ValidationError({"details":"passwords do not match"})
        
        try:
            validate_password(new_password1)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
                
        return super().validate(attrs)