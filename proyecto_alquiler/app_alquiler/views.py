from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import Contacto, PerfilUsuario, Alquiler, Usuario
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import  UsuarioRegistro, AlquilerCanchaForm, AlquilerSalonForm
from datetime import date
from django.contrib.auth.models import User

# Create your views here.

def es_admin(function=None, redirect_to=None):
    """Funcion para evaluar si el usuario es staff o no, se usara como deorador personalizado"""
    actual_decorator = user_passes_test(
        lambda u: u.is_staff,
        login_url=redirect_to,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def IndexView(request):
    'Pagina principal'
    return render(request, 'index.html')

def envio_formulario_contacto(request):
    """Para enviar el formulario de contacto la pagina principal"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        celular = request.POST.get('celular')
        consulta = request.POST.get('consulta')
        
        contacto = Contacto.objects.create(nombre=nombre, email=email, celular=celular, consulta=consulta)
        
        return redirect('index.html') 
    
    return redirect('index.html') 
 


def iniciar_sesion(request):
    """Inicio de sesion que recibe el login del usuario"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    return render(request, 'login.html')

def register(request):
    """Funcion para el registro de usuario"""
    data = {'form': UsuarioRegistro()}
    if request.method == 'POST':
        user_creation_form = UsuarioRegistro(data=request.POST)
        if user_creation_form.is_valid():
            user = user_creation_form.save()
            perfil_usuario = PerfilUsuario(usuario=user, celular=user_creation_form.cleaned_data['celular'])
            perfil_usuario.save()
            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return HttpResponseRedirect(reverse("Index") + "?delay=4")
        else:
            data['form'] = user_creation_form
    return render(request, 'registro.html', data)


def perfil_usuario(request):
    """Obtiene el usuario actual, esto es para poder obrener los datos de perfil del mismo 
    ademas del celular de la tabla relacionada"""
    perfil_usuario = PerfilUsuario.objects.get(usuario=request.user)
    celular = perfil_usuario.celular
    return render(request, 'perfil.html', {'perfil_usuario': perfil_usuario})

def inicio_sesion(request):
    return render(request, 'login.html')

def exit(request):
    """Desloguea al usuario"""
    logout(request)
    return redirect(reverse("Index"))

@login_required
def perfil(request):
    """Vista del perfil de usuario, recibe los datos del mismo y los alquileres, filtra los mismos en 2 listas"""
    usuario = request.user
    alquileres = Alquiler.objects.filter(usuario=usuario)  
    alquileres_vigentes = alquileres.filter(fecha_alquiler__gte=date.today()).order_by('-fecha_alquiler')
    alquileres_finalizados = alquileres.filter(fecha_alquiler__lt=date.today()).order_by('-fecha_alquiler')

    context = {
        'usuario' : usuario,
        'alquileres' : alquileres,
        'alquileres_vigentes': alquileres_vigentes,
        'alquileres_finalizados': alquileres_finalizados,
    }
    return render(request, 'perfil.html', context)

@login_required
def alquiler(request):
    """recibe los datos del formulario alquiler y crea los alquileres en consecuencia"""
    alquiler_exitoso = False
    if request.method == 'POST':
        if 'alquilar_cancha' in request.POST:
            form_cancha = AlquilerCanchaForm(request.POST, user=request.user)
            form_salon = AlquilerSalonForm(initial={'usuario': request.user})
            if form_cancha.is_valid():
                alquiler = form_cancha.save()
                alquiler_exitoso = True
        elif 'alquilar_salon' in request.POST:
            form_salon = AlquilerSalonForm(request.POST, user=request.user)
            form_cancha = AlquilerCanchaForm(initial={'usuario': request.user})
            if form_salon.is_valid():
                alquiler = form_salon.save()
                alquiler_exitoso = True
    else:
        form_cancha = AlquilerCanchaForm(user=request.user)
        form_salon = AlquilerSalonForm(initial={'usuario': request.user})

    return render(request, 'alquiler.html', {
        'form_cancha': form_cancha,
        'form_salon': form_salon,
        'alquiler_exitoso': alquiler_exitoso
    })


@login_required
def alquilar_cancha(request):
    """Guarda el alquiler de una cancha"""
    if request.method == 'POST':
        form = AlquilerCanchaForm(request.POST, user=request.user)
        if form.is_valid():
            alquiler = form.save(commit=False)
            alquiler.usuario = request.user
            alquiler.save()
            return redirect('alquiler_exitoso')
    else:
        form = AlquilerCanchaForm(user=request.user)
    return render(request, 'alquiler.html', {'form_cancha': form})

@login_required
def alquilar_salon(request):
    """Guarda el alquiler de salon"""
    if request.method == 'POST':
        form = AlquilerSalonForm(request.POST, user=request.user)
        if form.is_valid():
            alquiler = form.save(commit=False)
            alquiler.usuario = request.user
            alquiler.save()
            return redirect('alquiler_exitoso')
    else:
        form = AlquilerSalonForm(user=request.user)
    return render(request, 'alquiler.html', {'form_salon': form})

def alquiler_exitoso(request):
    """Informa del alquier exitoso"""
    return render(request, 'Index')

@login_required
def eliminar_alquiler(request, id):
    """Recibe el id de un alquiler especifico y lo elimina"""
    if request.method == 'POST':
        alquiler = get_object_or_404(Alquiler, id=id)
        alquiler.delete()
        return JsonResponse({'message': 'Alquiler eliminado satisfactoriamente.'}, status=200)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
    
@es_admin(redirect_to=reverse_lazy('sin_permiso_user'))
def perfiladmin(request):
    """Perfil de administrador, permite gestionar usuarios y alquileres"""
    usuario = request.user
    alquileres = Alquiler.objects.all().order_by('fecha_alquiler') 
    todos_usuarios = User.objects.all().order_by('id')
    for alquiler in alquileres:
        usuario = User.objects.get(id=alquiler.usuario_id)
    alquileres_vigentes = alquileres.filter(fecha_alquiler__gte=date.today())
    alquileres_finalizados = alquileres.filter(fecha_alquiler__lt=date.today())

    context = {
        'usuario' : usuario,
        'alquileres' : alquileres,
        'todos_usuarios': todos_usuarios,
        'alquileres_vigentes': alquileres_vigentes,
        'alquileres_finalizados': alquileres_finalizados,

    }
    return render(request, 'perfiladmin.html', context)

@es_admin(redirect_to=reverse_lazy('sin_permiso_user'))
def eliminar_usuario(request, id):
    """Recibe el id del usuario y lo elimina"""
    if request.method == 'POST':
        usuario = get_object_or_404(User, id=id)
        usuario.delete()
        return JsonResponse({'message': 'Usuario eliminado satisfactoriamente.'}, status=200)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
    
@es_admin(redirect_to=reverse_lazy('sin_permiso_user'))
def editar_salon(request, id):
    """Recibe el id del alquiler de un salon y permite editar su informacion"""
    editando = get_object_or_404(Alquiler, id=id)
    
    if request.method == 'POST':
        form = AlquilerSalonForm(request.POST, instance=editando)
        if form.is_valid():
            form.save()
            messages.success(request, 'Los cambios se han guardado correctamente.')
            return redirect('perfiladmin')  
    else:
        form = AlquilerSalonForm(instance=editando)

    context = {
        'form': form,
        'editando': editando,
    }
    return render(request, 'editar_salon.html', context)

@es_admin(redirect_to=reverse_lazy('sin_permiso_user'))
def editar_cancha(request, id):
    """Recibe el id del aquiler de una cancha y permite editar su informacion"""
    editando = get_object_or_404(Alquiler, id=id)
    
    if request.method == 'POST':
        form = AlquilerCanchaForm(request.POST, instance=editando)
        if form.is_valid():
            form.save()
            messages.success(request, 'Los cambios se han guardado correctamente.')
            return redirect('perfiladmin')  
    else:
        form = AlquilerCanchaForm(instance=editando)

    context = {
        'form': form,
        'editando': editando,
    }
    return render(request, 'editar_cancha.html', context)

@es_admin(redirect_to=reverse_lazy('sin_permiso_user'))
def editar_usuario(request, id):
    """Recibe el id deun usuario y permite editar su informacion"""
    editando = get_object_or_404(User, id=id)
    
    if request.method == 'POST':
        form = UsuarioRegistro(request.POST, instance=editando)
        if form.is_valid():
            user = form.save()  # Guarda el usuario actualizado
            perfil_usuario = PerfilUsuario.objects.get_or_create(usuario=user)[0]  # Obtiene o crea el perfil de usuario
            perfil_usuario.celular = form.cleaned_data['celular']  # Actualiza el campo celular en el perfil de usuario
            perfil_usuario.save()  # Guarda el perfil de usuario actualizado
            messages.success(request, 'Los cambios se han guardado correctamente.')
            return redirect('perfiladmin')  
    else:
        form = UsuarioRegistro(instance=editando)

    context = {
        'form': form,
        'editando': editando,
    }
    return render(request, 'editar_usuario.html', context)

def sin_permiso_user(request):
    """En caso que un usuario que no sea staff quiera acceder a una vista protegida lo envia a esta vista de error"""
    return render(request,'sin_permiso_user.html')


   
    
