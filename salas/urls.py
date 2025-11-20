from django.urls import path
from . import views

app_name = 'salas'

urlpatterns = [
    path('', views.lista_salas, name='lista_salas'),
    path('sala/<int:pk>/', views.detalle_sala, name='detalle_sala'),
    path('sala/<int:pk>/reservar/', views.crear_reserva, name='crear_reserva'),
    path('reserva/<int:pk>/exitosa/', views.reserva_exitosa, name='reserva_exitosa'),
]