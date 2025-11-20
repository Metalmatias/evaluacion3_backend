from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class Sala(models.Model):
    nombre = models.CharField(max_length=50)
    capacidad_maxima = models.PositiveIntegerField()
    habilitada = models.BooleanField(default=True)
    

    class Meta:
        #
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
    
    def esta_disponible(self):
        #muestra true si la sala esta disponible en el momento
        ahora = timezone.now()
        return not self.reservas.filter(
            hora_inicio__lte = ahora,
            hora_termino__gt = ahora
        ).exists()
    
class Reserva(models.Model):
    rut = models.CharField(max_length=12, help_text='formato: 12.345.678-9')
    hora_inicio = models.DateTimeField(default=timezone.now)
    hora_termino = models.DateTimeField()
    sala = models.ForeignKey(
        Sala,
        on_delete=models.CASCADE,
        related_name='reservas'
    )
    
    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-hora_inicio']
    
    def __str__(self):
        return f"reserva {self.sala.nombre} - {self.rut}" 

    def save(self, *args, **kwargs):
        if not self.pk:
            self.hora_termino = self.hora_inicio + timedelta(hours=2)
        super().save(*args, **kwargs)   
            
    