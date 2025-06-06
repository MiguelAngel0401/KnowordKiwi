import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
        try:
            data = request.data
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return Response({'error': 'Correo electrónico y contraseña son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(email=email).first()

            if not user or not user.check_password(password):
                return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

            if not user.is_active:
                return Response({'error': 'Esta cuenta está desactivada'}, status=status.HTTP_403_FORBIDDEN)

            return Response({'message': 'Inicio de sesión exitoso', 'user_id': str(user.id)}, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error en el servidor:", str(e))
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
