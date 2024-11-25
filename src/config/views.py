from tempfile import template

from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, update_session_auth_hash, login as login_django
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required

from apps.utils.decorators import verificar_permisos


@login_required
# @verificar_permisos()
def mi_pagina_inicio(request):
    template_name = 'mi_pagina_inicio.html'
    

    ctx = {
        "usuario_autenticado": request.user.first_name,
        "TITULO": "INICIO"
    }
    return render(request, template_name, ctx)


def login(request):
    # print("=========================")
    # print("method", request.method)
    # print(request)
    # print(request.__class__.__name__)
    # print(request.__dict__)
    """
    print("PARAMETROS GET--> ", request.GET)
    username = request.GET.get("username", default=None)
    password = request.GET.get("password", default=None)    
    """
    se_autentico = False
    salio_mal = True
    username = ""
    if request.method == "POST":
        username = request.POST.get("username", default=None)
        password = request.POST.get("password", default=None)
        usuario = authenticate(request, username=username, password=password)
        se_autentico = True
        if usuario:
            salio_mal = False
            login_django(request, usuario)
            return redirect("inicio")
        else:
            print("autenticacion mal")

    ctx = {
        "se_autentico": se_autentico,
        "salio_mal": salio_mal,
        "username": username
    }
    return render(request, 'login.html', ctx)


class BaseTemplateView(TemplateView):
    template_name = "blank.html"


def pagina_error_permisos(request):
    template_name = 'paginas/error_permisos.html'

    ctx = {
    }
    return render(request, template_name, ctx)