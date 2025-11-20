from django.contrib import admin
from .models import Sala, Reserva

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'capacidad_maxima', 'habilitada', 'disponibilidad_actual']
    list_filter = ['habilitada']
    search_fields = ['nombre']
    ordering = ['nombre']
    
    def disponibilidad_actual(self, obj):
        disponible = obj.esta_disponible()
        return "✅ Disponible" if disponible else "❌ Ocupada"
    disponibilidad_actual.short_description = 'Estado Actual'

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['sala', 'rut', 'hora_inicio', 'hora_termino', 'en_curso']
    list_filter = ['sala', 'hora_inicio']
    search_fields = ['rut', 'sala__nombre']
    readonly_fields = ['hora_inicio',]
    
    def en_curso(self, obj):
        from django.utils import timezone
        ahora = timezone.now()
        return obj.hora_inicio <= ahora < obj.hora_termino
    en_curso.boolean = True
    en_curso.short_description = 'En Curso'