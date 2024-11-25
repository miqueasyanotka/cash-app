from django.db import models

from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    dni = models.IntegerField(null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    es_admin = models.BooleanField(default=False)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cuenta_activa = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.id} - {self.username}. {self.first_name} - {self.last_name}"
    


class Cuenta(models.Model):
    # usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cuentas_frecuentes = models.ManyToManyField(Usuario, related_name='cuentas_frecuentes', blank=True)
    
    def __str__(self):
        # return f"Cuenta de {self.usuario.username}"
        return f"Cuenta de {self.usuario.username} - Saldo: {self.saldo}"
    