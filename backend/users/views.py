import json
import uuid
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import User

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        try:
            
            data = json.loads(request.body)

            email = data.get('email')
            username = data.get('username')
            real_name = data.get('real_name')
            password = data.get('password')
            

            if not all([email, username, real_name, password]):
                return JsonResponse({'error': 'Todos los campos deben estar llenos'}, status=400)
            

            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'El correo electrónico ya está registrado'}, status=400)
            

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'El nombre de usuario ya existe'}, status=400)
            

            user = User.objects.create_user(
                email=email,
                username=username,
                real_name=real_name,
                password=password,
                email_verification_token=str(uuid.uuid4())  
                
            )

            return JsonResponse({'message': 'Usuario registrado correctamente.', 'user_id': str(user.id)}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
