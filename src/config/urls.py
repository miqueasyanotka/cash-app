"""
URL configuration for appbank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as views_django
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('inicio/', views.mi_pagina_inicio, name="inicio"),
    path('', views.mi_pagina_inicio, name="inicio"),

    path('base', views.BaseTemplateView.as_view(), name='base'),

    # path('login/', views.login, name="login"),
    # path('login/', views_django.LoginView.as_view(), name="login"),
    path('login/', views_django.LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', views_django.logout_then_login, name="logout"),

    path("error-permisos", views.pagina_error_permisos, name="error_permisos"),
    
    # path('api/v1/', include(apis_urls)),

    # path('usuarios/lista/', views.lista_usuarios, name="lista_de_usuarios"),
    path('usuarios/', include("apps.usuarios.urls")),
    path('transacciones/', include("apps.transacciones.urls")),
    # path('pacientes/', include("apps.pacientes.urls")),
    # path('vacunas/', include("apps.vacunas.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)