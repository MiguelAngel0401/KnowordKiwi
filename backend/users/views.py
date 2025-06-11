from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserLoginSerializer, UserRegistrationSerializer

User = get_user_model()

#UwU

# Vista de registro
import secrets
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generar token de verificación
            token = secrets.token_urlsafe(32)
            user.email_verification_token = token
            user.email_verification_expires_at = timezone.now() + timezone.timedelta(hours=24)
            user.save()

            # Construir URL de verificación
            verification_url = request.build_absolute_uri(
                reverse("verify-email", args=[token])
            )

            # Enviar correo de verificación
            send_mail(
                subject="Verifica tu correo electrónico",
                message=f"Hola {user.username}, por favor verifica tu correo haciendo clic en el siguiente enlace:\n{verification_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return Response(
                {"message": "Usuario registrado correctamente. Revisa tu correo para verificar tu cuenta."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista de login
class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            user = serializer.validated_data["user"]

            # Opcional: evitar login si no ha verificado su correo
            if not user.is_email_verified:
                return Response(
                    {"error": "Por favor verifica tu correo antes de iniciar sesión."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista de verificación de correo
class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            user = User.objects.get(email_verification_token=token)

            if (
                user.email_verification_expires_at
                and user.email_verification_expires_at < timezone.now()
            ):
                return Response(
                    {"error": "El token de verificación ha expirado."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.is_email_verified = True
            user.email_verification_token = None
            user.email_verification_expires_at = None
            user.save()

            return Response(
                {"message": "Correo verificado correctamente."},
                status=status.HTTP_200_OK,
            )

        except User.DoesNotExist:
            return Response(
                {"error": "Token inválido o usuario no encontrado."},
                status=status.HTTP_400_BAD_REQUEST,
            )
