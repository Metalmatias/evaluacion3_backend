from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Sala, Reserva
from .forms import ReservaForm

def lista_salas(request):
    salas = Sala.objects.filter(habilitada=True)
    ahora = timezone.now()
    
    for sala in salas:
        reserva_actual = sala.reservas.filter(
            hora_inicio__lte=ahora,
            hora_termino__gt=ahora
        ).first()
        sala.reserva_actual = reserva_actual
    
    context = {
        'salas': salas,
        'ahora': ahora,
    }
    return render(request, 'salas/lista_salas.html', context)

def detalle_sala(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    ahora = timezone.now()
    
    reserva_actual = sala.reservas.filter(
        hora_inicio__lte=ahora,
        hora_termino__gt=ahora
    ).first()
    
    context = {
        'sala': sala,
        'reserva_actual': reserva_actual,
    }
    return render(request, 'salas/detalle_sala.html', context)

def crear_reserva(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    
    if not sala.esta_disponible():
        messages.error(request, f"La sala '{sala.nombre}' no está disponible.")
        return redirect('salas:lista_salas')
    
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.sala = sala
            reserva.save()
            messages.success(request, f'Reserva creada exitosamente para la sala {sala.nombre}')
            return redirect('salas:reserva_exitosa', pk=reserva.pk)
    else:
        form = ReservaForm(initial={'sala': sala})
    
    context = {
        'form': form,
        'sala': sala,
    }
    return render(request, 'salas/crear_reserva.html', context)

def reserva_exitosa(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    context = {'reserva': reserva}
    return render(request, 'salas/reserva_exitosa.html', context)