from django import forms
from .models import MotivoTransferencia, Transferencia, Deposito
from apps.usuarios.models import Usuario


class MotivoTransferenciaForm(forms.ModelForm):
    class Meta:
        model = MotivoTransferencia
        fields = ['nombre']
        
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        # Verificar si ya existe un motivo con el mismo nombre
        if MotivoTransferencia.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError("Ya existe un motivo con este nombre.")
        return nombre
        
        
class FavoritosForm(forms.Form):
    receptor = forms.ModelChoiceField(queryset=Usuario.objects.all(), label="Selecciona una cuenta favorita", required=True)
    
    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario')  # Para que se pase el usuario desde la vista
        super().__init__(*args, **kwargs)
        # Excluir al mismo usuario de ser su propio favorito
        self.fields['receptor'].queryset = Usuario.objects.exclude(id=usuario.id)


class TransferenciaForm(forms.ModelForm):
    class Meta:
        model = Transferencia
        fields = ['monto', 'motivo']


class DepositoForm(forms.ModelForm):
    class Meta:
        model = Deposito
        fields = ['monto']
        widgets = {
            'monto': forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Monto a ingresar'}),
        }