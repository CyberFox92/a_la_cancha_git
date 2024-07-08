"""
URL configuration for proyecto_alquiler project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from app_alquiler.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView, name="Index"),
    path('', envio_formulario_contacto, name='envio_formulario_contacto'),
    path('inicio_sesion', iniciar_sesion, name='iniciar_sesion'),
    path('registrar', register, name='registro'),
    path('iniciar', inicio_sesion, name='iniciar'),
    path('exit', exit, name='exit'),
    path('perfil', perfil, name="perfil"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('perfil_usuario', perfil_usuario, name='perfil_usuario'),
    path('alquiler', alquiler, name='alquiler'),
    path('alquilar_cancha/', alquilar_cancha, name='alquilar_cancha'),
    path('alquilar_salon/', alquilar_salon, name='alquilar_salon'),
    path('alquiler_exitoso/', alquiler_exitoso, name='alquiler_exitoso'),
    path('eliminar-alquiler/<int:id>/', eliminar_alquiler, name='eliminar_alquiler'),   
    path('perfiladmin', perfiladmin, name='perfiladmin'),
    path('eliminar-usuario/<int:id>/', eliminar_usuario, name='eliminar_usuario'),
    path('editar_salon/<int:id>/', editar_salon, name='editar_salon'),  
    path('editar_cancha/<int:id>/', editar_cancha, name='editar_cancha'),  
    path('editar_usuario/<int:id>/', editar_usuario, name='editar_usuario'),  
    path('sin_permiso_user/', sin_permiso_user, name='sin_permiso_user'),      

]