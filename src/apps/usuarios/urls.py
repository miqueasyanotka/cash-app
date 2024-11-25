from django.urls import path, include

from . import views

app_name = "usuarios"

urlpatterns = [
    path('lista/', views.lista_usuarios, name="lista"),
    path('nuevo/', views.nuevo, name="nuevo"),
    path('detalle/<int:usuario_id>/', views.detalle, name="detalle"),
    path('editar/<int:usuario_id>/', views.editar_usuario, name="editar"),
    path('eliminar/<int:usuario_id>/', views.eliminar_usuario, name="eliminar"),
    
    path('editar_datos/<int:usuario_id>/', views.editar_datos_usuario, name='editar_datos'),
    path('cambiar_contrasena/<int:usuario_id>/', views.cambiar_contrasena_usuario, name='cambiar_contrasena'),
    
]