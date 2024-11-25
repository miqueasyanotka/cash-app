from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from .models import Usuario

class FormUsuario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['password', 'username', 'first_name', 'last_name', 'email', 'is_active', 'dni']
     
        
class FormUser(UserCreationForm):
    username  = forms.CharField(label="Nombre de usuario", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre de usuario'}))
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'es_admin', 'dni']


    def __init__(self, *args, **kwargs):
        super(FormUser, self).__init__(*args, **kwargs)
        
        add_class_form_control = ["first_name", "username", "last_name", "email", "dni", "password1", "password2"]
        
        for attr_field in add_class_form_control:
            self.fields[attr_field].widget.attrs['class'] = 'form-control'
            
    def clean_dni(self):
        dni = self.cleaned_data["dni"]
        if not (7 <= len(str(dni)) <=8):
            raise ValidationError("El DNI debe tener entre 7 y 8 caracteres númericos.")
        print(dni.__class__.__name__)
        return dni
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Verifica si el nombre de usuario ya existe, excepto para el usuario actual
        if Usuario.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Ya existe un usuario con ese nombre.")
        return username


class FormUsuarioSinPassword(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'es_admin', 'dni']

class FormUsuarioParaUsuario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'dni']
        
class FormUsuarioConPassword(PasswordChangeForm):
    class Meta:
        model = Usuario
        fields = ['old_password','password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['new_password1'])
        if commit:
            user.save()
        return user;
     