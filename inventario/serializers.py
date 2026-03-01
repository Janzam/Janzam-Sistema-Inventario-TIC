from rest_framework import serializers
from .models import Equipo

class EquipoSerializer(serializers.ModelSerializer):
    # Definimos creado_por como solo lectura para que no lo pida en el formulario
    creado_por = serializers.ReadOnlyField(source='creado_por.username')

    class Meta:
        model = Equipo
        fields = '__all__'

    def validate_serie(self, value):
        # Convertimos a mayúsculas para comparar correctamente
        serie_nueva = value.upper().strip()
        
        # Verificamos si ya existe, EXCLUYENDO el equipo actual si estamos editando
        instance = getattr(self, 'instance', None)
        qs = Equipo.objects.filter(serie__iexact=serie_nueva)
        
        if instance:
            qs = qs.exclude(pk=instance.pk)
            
        if qs.exists():
            raise serializers.ValidationError("Error: Esta Serie ya pertenece a otro equipo registrado.")
            
        return serie_nueva