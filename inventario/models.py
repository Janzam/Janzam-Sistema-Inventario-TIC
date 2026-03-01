from django.db import models
from django.conf import settings

class Equipo(models.Model):
    # Relación con el usuario para privacidad
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='mis_equipos',
        null=True, 
        blank=True
    )

    ESTADOS = [
        ('DISPONIBLE', 'Disponible'),
        ('ASIGNADO', 'Asignado'),
        ('REPARACION', 'En Reparación'),
        ('BAJA', 'Baja'),
        ('NUEVO', 'Nuevo'),
    ]

    nombre_equipo = models.CharField(max_length=100)
    serie = models.CharField(max_length=100, unique=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    activo_fijo = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    estado = models.CharField(max_length=20, choices=ESTADOS, default='NUEVO')
    usuario_asignado = models.CharField(max_length=100, blank=True, null=True)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    
    novedad = models.TextField(blank=True, null=True)
    fecha_ingreso = models.DateField(null=True, blank=True)
    fecha_baja = models.DateField(null=True, blank=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre_equipo', 'serie']

    def save(self, *args, **kwargs):
        if self.nombre_equipo:
            self.nombre_equipo = self.nombre_equipo.upper().strip()
        if self.serie:
            self.serie = self.serie.upper().strip()

        user = getattr(self, 'usuario_asignado', None)
        status = getattr(self, 'estado', 'NUEVO')

        if not user or user.strip() == "":
            if status not in ['NUEVO', 'BAJA', 'REPARACION']:
                self.estado = 'DISPONIBLE'
        elif user and status in ['DISPONIBLE', 'NUEVO']:
            self.estado = 'ASIGNADO'

        super(Equipo, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_equipo} ({self.serie})"