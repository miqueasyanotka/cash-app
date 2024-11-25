from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from decimal import Decimal
from apps.usuarios.models import Usuario
from django.core.paginator import Paginator
from django.db.models import Sum
from django.utils.timezone import now
from .forms import MotivoTransferenciaForm, FavoritosForm,DepositoForm
from django.http import HttpResponseServerError



@login_required
def ver_saldo(request):
    template_name = 'transacciones/ver_saldo.html'

    saldo_actual = request.user.saldo

    depositos = Deposito.objects.filter(usuario=request.user).order_by('-fecha')
    transferencias_recibidas = Transferencia.objects.filter(receptor=request.user).aggregate(total_recibido=Sum('monto'))
    transferencias_realizadas = Transferencia.objects.filter(emisor=request.user).aggregate(total_enviado=Sum('monto'))

    context = {
        'saldo_actual': saldo_actual,
        'depositos': depositos,
        'transferencias_recibidas': transferencias_recibidas.get('total_recibido', 0) or 0,
        'transferencias_realizadas': transferencias_realizadas.get('total_enviado', 0) or 0,
    }
    return render(request, template_name, context)


@login_required
def ingresar_dinero(request):
    template_name = 'transacciones/ingresar_dinero.html'

    if request.method == 'POST':
        form = DepositoForm(request.POST)
        if form.is_valid():
            deposito = form.save(commit=False)
            deposito.usuario = request.user  # Asigna el usuario actual al depósito
            deposito.save()

            # Obtener el saldo actual del usuario y actualizarlo
            usuario = request.user
            monto = deposito.monto 
            
            monto = Decimal(monto)
            
            # Sumar el monto al saldo actual del usuario
            usuario.saldo += monto
            usuario.save()

            messages.success(request, "Depósito realizado con éxito.")
            return redirect('transacciones:ver_saldo')
    else:
        form = DepositoForm()

    context = {
        'form': form,
    }
    return render(request, template_name, context)



@login_required
def transferir_dinero_favorito(request, favorito_id):
    template_name = 'transacciones/transferir_dinero_favorito.html'

    try:
        # Obtener la cuenta favorita
        cuenta_favorita = get_object_or_404(CuentaFavorita, id=favorito_id, usuario=request.user)
        receptor = cuenta_favorita.favorito 
        emisor = request.user

        if emisor.id == receptor.id:
            raise ValueError("El receptor asociado a esta cuenta favorita es el mismo que el usuario emisor. Revisa la configuración de tus cuentas favoritas.")

        print(f"Emisor: ID={emisor.id}, Username={emisor.username}")
        print(f"Receptor: ID={receptor.id}, Username={receptor.username}")

        if request.method == 'POST':
            monto = request.POST.get('monto')
            motivo_id = request.POST.get('motivo')

            # Validar los campos
            if not monto or not motivo_id:
                raise ValueError("Todos los campos son obligatorios.")

            monto = Decimal(monto)
            motivo = get_object_or_404(MotivoTransferencia, id=motivo_id)

            if emisor.saldo < monto:
                raise ValueError("Saldo insuficiente.")

            emisor.saldo -= monto
            receptor.saldo += monto

            emisor.save()
            receptor.save()

            print(f"Saldo del emisor después de guardar: {Usuario.objects.get(id=emisor.id).saldo}")
            print(f"Saldo del receptor después de guardar: {Usuario.objects.get(id=receptor.id).saldo}")

            # Registrar la transferencia
            transferencia = Transferencia.objects.create(
                emisor=emisor,
                receptor=receptor,
                monto=monto,
                motivo=motivo,
                fecha_transferencia=now(),
            )

            messages.success(request, "Transferencia realizada con éxito.")
            return redirect('transacciones:ver_comprobante', tipo='transferencia', transaccion_id=transferencia.id)

        return render(request, template_name, {
            'cuenta_favorita': cuenta_favorita,
            'motivos': MotivoTransferencia.objects.all(),
        })

    except Exception as e:
        print("Error durante la transferencia:", e)
        messages.error(request, f"Ocurrió un error: {e}")
        return redirect('transacciones:transferir_dinero_favorito', favorito_id=favorito_id)

@login_required
def transferir_dinero(request):
    template_name = 'transacciones/transferir_dinero.html'

    try:
        if request.method == 'POST':
            receptor_username = request.POST.get('receptor')
            monto = request.POST.get('monto')
            motivo_id = request.POST.get('motivo')

            if not receptor_username or not monto or not motivo_id:
                raise ValueError("Todos los campos son obligatorios.")

            monto = Decimal(monto)
            receptor = get_object_or_404(Usuario, username=receptor_username)
            motivo = get_object_or_404(MotivoTransferencia, id=motivo_id)

            emisor = request.user

            if emisor.saldo < monto:
                raise ValueError("Saldo insuficiente.")

            emisor.saldo -= monto
            receptor.saldo += monto

            emisor.save()
            receptor.save()

            transferencia = Transferencia.objects.create(
                emisor=emisor,
                receptor=receptor,
                monto=monto,
                motivo=motivo,
                fecha_transferencia=timezone.now(),  # Asignar la fecha actual
            )

            messages.success(request, "Transferencia realizada con éxito.")
            return redirect('transacciones:ver_comprobante', tipo='transferencia', transaccion_id=transferencia.id)

        return render(request, template_name, {
            'motivos': MotivoTransferencia.objects.all(),
            'usuarios': Usuario.objects.filter(is_active=True)
        })

    except Exception as e:
        # Registro de errores en consola
        print("Error durante la transferencia:", e)
        return HttpResponseServerError("Ocurrió un error: " + str(e))


@login_required
def ver_comprobante(request, tipo, transaccion_id):
    template_name = 'transacciones/ver_comprobante.html'
    
    if tipo == 'transferencia':
        transaccion = get_object_or_404(Transferencia, id = transaccion_id)
    elif tipo == 'deposito':
        transaccion = get_object_or_404(Deposito, id = transaccion_id)
        tipo = 'deposito'
    else:
        raise ValueError("tipo de transacción no válido")
    
    ctx = {
        'transaccion': transaccion,
        'tipo': tipo
    }
    return render(request, template_name, ctx)


@login_required
def historial(request):
    template_name = 'transacciones/historial.html'
    
    transferencias = Transferencia.objects.all()
    depositos = Deposito.objects.all()

    for transaccion in transferencias:
        transaccion.tipo = 'transferencia'
        transaccion.fecha_unificada = transaccion.fecha_transferencia  # Unificar campo de fecha
    
    for transaccion in depositos:
        transaccion.tipo = 'deposito'
        transaccion.fecha_unificada = transaccion.fecha  # Unificar campo de fecha

    transacciones = sorted(
        list(transferencias) + list(depositos),
        key=lambda x: x.fecha_unificada,
        reverse=True
    )

    paginator = Paginator(transacciones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, template_name, context)



@login_required
def listar_motivos(request):
    template_name = 'transacciones/listar_motivos.html'
    motivos = MotivoTransferencia.objects.all()
    
    # Paginación: 10 elementos por página
    paginator = Paginator(motivos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if (request.user.is_superuser or request.user.es_admin):
        ctx = {
            'page_obj': page_obj,
            'paginator': paginator,
            'motivos': motivos,
            'titulo' : "Lista de motivos"
        }
    else:
        ctx = {
            "error": "no tienes permisos",
            "titulo": "Lista de motivos"
        }
    return render(request, template_name, ctx)



@login_required
def crear_motivo(request):
    template_name = 'transacciones/crear_motivo.html'
    form = MotivoTransferenciaForm()
    
    message = ""
    if (request.user.is_superuser or request.user.es_admin) and request.method == 'POST':
        form = MotivoTransferenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transacciones:listar_motivos')
        else:
            message = "No se pudo guardar el motivo"
    
    ctx = {
        "formMotivo" : form,
        "messages" : message,
        "titulo": "Crear Motivo"
    }
    return render(request, template_name, ctx)
    
    
        
@login_required
def editar_motivo(request, motivo_id):
    template_name = 'transacciones/editar_motivo.html'
    motivo = get_object_or_404(MotivoTransferencia,id = motivo_id)
    form = None
    
    if (request.user.is_superuser or request.user.es_admin):
        if request.method == 'POST':
            form = MotivoTransferenciaForm(request.POST, instance = motivo)
            if form.is_valid():
                form.save()
                return redirect('transacciones:listar_motivos')
        else:
            form = MotivoTransferenciaForm(instance = motivo)
    else:
            ctx = {
            "formMotivo" : form,
            "messages" : "no tienes permisos",
            "titulo": "Editar Motivo"
    }
    ctx = {
        "formMotivo" : form,
        "titulo": "Editar Motivo"
    }
    
    return render(request, template_name, ctx)

    
    
    
@login_required
def eliminar_motivo(request, motivo_id):
    template_name = 'transacciones/eliminar_motivo.html'
    motivo = MotivoTransferencia.objects.get(id = motivo_id)
    
    if  (request.user.is_superuser or request.user.es_admin) and request.method == 'POST':
        motivo.delete()
        return redirect('transacciones:listar_motivos')
    
    ctx = {
        "motivo" : motivo,
        # "messages" : message,
        "titulo": "Eliminar Motivo"
    }
    return render(request, template_name, ctx)

    

@login_required
def marcar_favorito(request):
    template_name = 'transacciones/marcar_favorito.html'
    
    favoritos = CuentaFavorita.objects.filter(usuario=request.user).exclude(favorito=request.user)

    usuarios_disponibles = Usuario.objects.exclude(id=request.user.id).exclude(id__in=favoritos.values('favorito'))

    if request.method == 'POST':
        form = FavoritosForm(request.POST, usuario=request.user)
        if form.is_valid():
            receptor = form.cleaned_data['receptor']
            
            if receptor != request.user and not CuentaFavorita.objects.filter(usuario=request.user, favorito=receptor).exists():
                CuentaFavorita.objects.create(usuario=request.user, favorito=receptor)
            return redirect('transacciones:marcar_favorito')  # Redirigir a la misma vista para mostrar los favoritos actualizados
    else:
        form = FavoritosForm(usuario=request.user)

    paginator = Paginator(favoritos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    ctx = {
        'page_obj': page_obj,
        'paginator': paginator,
        'form': form,
        'favoritos': favoritos,  
        'usuarios_disponibles': usuarios_disponibles
        
    }

    return render(request, template_name, ctx)


    

@login_required
def eliminar_favorito(request, favorito_id):
    cuenta_favorita = CuentaFavorita.objects.filter(usuario=request.user, id=favorito_id).first()

    if cuenta_favorita:
        cuenta_favorita.delete()

    return redirect('transacciones:marcar_favorito') 
