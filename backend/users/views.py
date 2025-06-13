

from django.shortcuts import render

from django.http import HttpResponse

def home(request):
    return HttpResponse("¡Pruebas Users!")

import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserLoginSerializer
from .models import User

class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data

            email = data.get('email')
            username = data.get('username')
            real_name = data.get('real_name')
            password = data.get('password')

            if not all([email, username, real_name, password]):
                return Response({'error': 'Todos los campos deben estar llenos'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=email).exists():
                return Response({'error': 'El correo electrónico ya está registrado'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=username).exists():
                return Response({'error': 'El nombre de usuario ya existe'}, status=status.HTTP_400_BAD_REQUEST)

            # Marcos esta funcion crea el usuario sin el token
            user = User.objects.create_user(
                email=email,
                username=username,
                real_name=real_name,
                password=password
            )

            # Ahora aqui guarda el token del usuario
            user.email_verification_token = str(uuid.uuid4())
            user.save()

            return Response({'message': 'Usuario registrado correctamente.', 'user_id': str(user.id)}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("Error en el servidor:", str(e))
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        #Apartir de aqui porgramas la logica del loginview va 


class LoginView(APIView):
    def post(self, request):

        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

