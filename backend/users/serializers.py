from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import uuid
from django.conf import settings


# Serializdor de Login
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )

            if not user:
                raise serializers.ValidationError(
                    "Credenciales inválidas, intenta de nuevo."
                )
            if not user.is_active:
                raise serializers.ValidationError("Esta cuenta está desactivada.")
        else:
            raise serializers.ValidationError("Se requiere correo y contraseña.")

        data["user"] = user
        return data


# Serializador de Registro


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("email", "username", "real_name", "password")

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Este correo electrónico ya está registrado."
            )
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya existe.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        # Crear token y expiración
        user.email_verification_token = str(uuid.uuid4())
        user.email_verification_expires_at = timezone.now() + timedelta(hours=24)
        user.save()

        # Construir el enlace de verificación
        verification_url = (
            f"http://localhost:8000/api/verify-email/{user.email_verification_token}/"
        )

        # Enviar correo
        send_mail(
            subject="Verifica tu correo",
            message=f"Hola {user.username}, haz clic en el siguiente enlace para verificar tu correo:\n{verification_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return user


# Serializador de Usuario
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "email_verification_token",
            "email_verification_expires_at",
            "password_reset_token",
            "password_reset_expires_at",
        )
