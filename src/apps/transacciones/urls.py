from django.urls import path

from . import views

app_name = "transacciones"

urlpatterns = [
    
    path('ver_saldo/', views.ver_saldo, name="ver_saldo"),
    path('ingresar_dinero/', views.ingresar_dinero, name="ingresar_dinero"),
    path('transferir_dinero/', views.transferir_dinero, name="transferir_dinero"),
    path('transferir_dinero_favorito/<int:favorito_id>/', views.transferir_dinero_favorito, name='transferir_dinero_favorito'),
    path('historial/', views.historial, name="historial"),
    path('comprobante/<str:tipo>/<int:transaccion_id>/', views.ver_comprobante, name='ver_comprobante'),

    path('motivos/', views.listar_motivos, name='listar_motivos'),
    path('motivos/crear/', views.crear_motivo, name='crear_motivo'),
    path('motivos/editar/<int:motivo_id>/', views.editar_motivo, name='editar_motivo'),
    path('motivos/eliminar/<int:motivo_id>/', views.eliminar_motivo, name='eliminar_motivo'),
    
    path('marcar-favorito/', views.marcar_favorito, name='marcar_favorito'),
    path('eliminar-favorito/<int:favorito_id>', views.eliminar_favorito, name='eliminar_favorito'),
    
]