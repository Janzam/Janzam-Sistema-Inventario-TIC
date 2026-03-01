from rest_framework import serializers
from .models import Equipo

class EquipoSerializer(serializers.ModelSerializer):
    creado_por = serializers.ReadOnlyField(source='creado_por.username')
    class Meta:
        model = Equipo
        fields = '__all__'

    def validate_serie(self, value):
        serie_nueva = value.upper().strip()
        instance = getattr(self, 'instance', None)
        qs = Equipo.objects.filter(serie__iexact=serie_nueva)
        
        if instance:
            qs = qs.exclude(pk=instance.pk)
            
        if qs.exists():
            raise serializers.ValidationError("Error: Esta Serie ya pertenece a otro equipo registrado.")
            
        return serie_nueva