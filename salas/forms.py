from django import forms
from .models import Reserva, Sala

class ReservaForm(forms.ModelForm):
    class Meta: 
        model = Reserva
        fields = ['rut','sala']
        widgets = {
            'rut': forms.TextInput(attrs={
                'placeholder': '12.345.678-9',
                'class': 'form-control'
            }),
            'sala': forms.Select(attrs={'class':'form-control'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sala'].queryset = Sala.objects.filter(
            habilitada = True
        ).distinct()

    def limpiar_sala(self):
        sala = self.cleaned_data.get('sala')
        if sala and not sala.esta_disponible():
            raise forms.ValidationError(
                f"la sala '{sala.nombre}' no esta disponible en este momento"
            )
        return sala