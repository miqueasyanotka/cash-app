from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .forms import FormUser, FormUsuarioSinPassword, FormUsuarioConPassword, FormUsuarioParaUsuario
from .models import Usuario
from django.core.paginator import Paginator

@login_required
def nuevo(request):
    template_name = 'usuarios/nuevo_new.html'
    
    form = FormUser()
    message = ""
    if (request.user.is_superuser or request.user.es_admin) and request.method == 'POST':
        form = FormUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect("usuarios:lista")
        else:
            message = "No se pudo guardar de forma correcta el formulario"

    ctx = {
        "formUsuario": form,
        "message": message
    }
    return render(request, template_name, ctx)


@login_required
def detalle(request, usuario_id):
    template_name = 'usuarios/detalle.html'
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if (request.user.es_admin and usuario != request.user) or (usuario == request.user):
        ctx = {
            "usuario": usuario,
            "titulo": "Detalle de usuario"
        }
    else:
        ctx = {
            "error": "no tienes permisos para ver el detalle",
            "titulo": "Detalle de usuario"
        }
    return render(request, template_name, ctx)


@login_required
def lista_usuarios(request):
    template_name = 'usuarios/lista_new.html'
    
    if (request.user.is_superuser or request.user.es_admin):
        usuarios = Usuario.objects.all()
    else:
        usuarios = Usuario.objects.filter(id=request.user.id)
        
    paginator = Paginator(usuarios, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    ctx = {
        'page_obj': page_obj,
        'paginator': paginator,
        "usuarios": usuarios,
        "titulo": "LISTA DE USUARIOS"
    }
    return render(request, template_name, ctx)


@login_required
def editar_datos_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    template_name = 'usuarios/editar_datos.html'
    message = ""

    if (request.user.is_superuser or request.user.es_admin):
        form = FormUsuarioSinPassword(instance=usuario)
        if request.method == 'POST':
            form = FormUsuarioSinPassword(request.POST, instance=usuario)
            if form.is_valid():
                form.save()
                return redirect('usuarios:lista')
            else:
                message = "No se pudo actualizar la información del usuario"
        else:
            form = FormUsuarioSinPassword(instance=usuario)
    elif not request.user.es_admin:
        form = FormUsuarioParaUsuario(instance=usuario)
        if request.method == 'POST':
            form = FormUsuarioParaUsuario(request.POST, instance=usuario)
            if form.is_valid():
                form.save()
                return redirect('usuarios:lista')
            else:
                message = "No se pudo actualizar la información del usuario"
        
    else:
        return HttpResponseForbidden("No tienes permisos para realizar esta acción.")

    ctx = {
        'formUsuario': form,
        'message': message,
        'titulo': "Editar datos del usuario",
    }
    return render(request, template_name, ctx)


@login_required
def cambiar_contrasena_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    template_name = 'usuarios/cambiar_contrasena.html'
    message = ""

    if (request.user.is_superuser or request.user.es_admin) or usuario == request.user:
        if request.method == 'POST':
            form = FormUsuarioConPassword(user=usuario, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, usuario) 
                return redirect('usuarios:lista')
            else:
                message = "No se pudo actualizar la contraseña"
        else:
            form = FormUsuarioConPassword(user=usuario)
    else:
        return HttpResponseForbidden("No tienes permisos para realizar esta acción.")

    ctx = {
        'formContrasena': form,
        'message': message,
        'titulo': "Cambiar contraseña",
    }
    return render(request, template_name, ctx)



@login_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    template_name = 'usuarios/editar.html'
    message = ""

    if (request.user.is_superuser or request.user.es_admin) and usuario == request.user:
        form = FormUsuarioSinPassword(instance=usuario)
        if request.method == 'POST':
            form = FormUser(request.POST, instance=usuario)
            if form.is_valid():
                form.save()
                return redirect('usuarios:lista')
            else:
                message = "No se pudo actualizar la información del usuario"
    elif (request.user.es_admin and usuario != request.user) or (usuario == request.user):
        form = FormUsuarioSinPassword(instance=usuario)
        if request.method == 'POST':
            form = FormUsuarioSinPassword(request.POST, instance=usuario)
            if form.is_valid():
                form.save()
                return redirect('usuarios:lista')
            else:
                message = "No se pudo actualizar la información del usuario"
        

    ctx = {
        'formUsuario': form,
        'message': message,
        'titulo': "Editar usuario",
    }
    return render(request, template_name, ctx)



@login_required
def eliminar_usuario(request, usuario_id):
    template_name = 'usuarios/eliminar.html'

    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    if (request.user.is_superuser or request.user.es_admin) and usuario != request.user and request.method == 'POST':
        usuario.delete()
        return redirect('usuarios:lista')
    
    ctx = {
        'usuario':usuario,
        'titulo':"Eliminar usuario",
    }
    return render(request, template_name, ctx)