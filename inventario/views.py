# C:\Inventario_Tic\backend\inventario\views.py

import pandas as pd
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Importa tus modelos y serializadores
from .models import Equipo
from .serializers import EquipoSerializer

# --- VISTA PARA MANEJAR LOS EQUIPOS ---
class EquipoViewSet(viewsets.ModelViewSet):
    serializer_class = EquipoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtra para que el usuario solo vea sus propios equipos
        return Equipo.objects.filter(creado_por=self.request.user)

    def perform_create(self, serializer):
        # Asigna el usuario logueado automáticamente
        serializer.save(creado_por=self.request.user)

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        try:
            queryset = self.get_queryset()
            data = list(queryset.values(
                'nombre_equipo', 'serie', 'marca', 'modelo', 
                'activo_fijo', 'estado', 'usuario_asignado', 
                'departamento', 'fecha_ingreso'
            ))

            if not data:
                return Response({"error": "No hay datos para exportar"}, status=400)

            df = pd.DataFrame(data).fillna('')
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=Inventario.xlsx'

            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=500)

# --- VISTA PARA REGISTRO DE USUARIOS ---
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name', '')

    if not username or not password:
        return Response({"error": "Usuario y contraseña requeridos"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Este usuario ya existe"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name
        )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user": {"username": user.username, "name": user.first_name}
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)