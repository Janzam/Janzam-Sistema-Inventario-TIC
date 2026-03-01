from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
import json

# ID de cliente que obtendrás en Google Cloud Console
GOOGLE_CLIENT_ID = "603363809870-d90iejkft23sje39m6qnm2878el1cett.apps.googleusercontent.com"

@csrf_exempt
def google_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data.get('token')
            
            # Verificar el token con Google
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
            
            # Validar el dominio de la organización (Opcional pero recomendado)
            # if idinfo['hd'] != 'tuempresa.com':
            #     return JsonResponse({'error': 'Dominio no autorizado'}, status=403)

            # Aquí puedes buscar el usuario en tu base de datos o crearlo
            user_data = {
                'email': idinfo['email'],
                'name': idinfo['name'],
                'picture': idinfo['picture']
            }

            return JsonResponse({'status': 'success', 'user': user_data})
            
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Token inválido'}, status=400)
    return JsonResponse({'status': 'error'}, status=405)