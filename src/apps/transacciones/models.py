from django.db import models
from django.utils import timezone
from apps.usuarios.models import *
from apps.transacciones.models import *

# Create your models here.

class MotivoTransferencia(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nombre
    
class CuentaFavorita(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    favorito = models.ForeignKey(Usuario, related_name="favoritos", on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True)

    def __str__(self):
        return f"{self.usuario.username} a {self.favorito.username}"
    
    
class Transferencia(models.Model):
    emisor = models.ForeignKey(Usuario, related_name='transferencias_emitidas', on_delete=models.CASCADE, null=True)
    receptor = models.ForeignKey(Usuario, related_name='transferencias_recibidas', on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.ForeignKey(MotivoTransferencia, on_delete=models.CASCADE)
    fecha_transferencia = models.DateTimeField(auto_now_add=True)  # Solo esta opción

    def __str__(self):
        return f"Transferencia de {self.monto} de {self.emisor.username} a {self.receptor.username}"
    
class Deposito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Depósito de {self.monto} por {self.usuario.username} el {self.fecha}"
