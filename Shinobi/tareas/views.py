from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .forms import RegistroForm, CreatForm
from .models import Perfil, Actividad
# Create your views here.


def home(request):
    return render(request, 'home.html')



def inscripcion(request):
    if request.method == "GET":
        return render(request, "inscripcion.html", {
            "form": RegistroForm()
        })

    form = RegistroForm(request.POST)

    if form.is_valid():
        data = form.cleaned_data

        username = data["username"]
        email = data["email"]

        # 🚨 VALIDAR USERNAME
        if User.objects.filter(username=username).exists():
            return render(request, "inscripcion.html", {
                "form": form,
                "error": "El nombre de usuario ya existe"
            })

        # 🚨 VALIDAR EMAIL
        if User.objects.filter(email=email).exists():
            return render(request, "inscripcion.html", {
                "form": form,
                "error": "El correo ya está registrado"
            })

        # 👤 CREAR USUARIO
        user = User.objects.create_user(
            username=username,
            email=email,
            password=data["password1"]
        )

        # 🧠 CREAR PERFIL
        Perfil.objects.create(
            user=user,
            numero=data["numero"],
            documento=data["documento"],
            plan=data["plan"]
        )

        login(request, user)
        return redirect("tareas")

    return render(request, "inscripcion.html", {
        "form": form
    })
@login_required
def tareas(request):
    perfil = Perfil.objects.filter(user=request.user).first()  # 🔥 traes datos del usuario
    actividades = Actividad.objects.filter(user=request.user, f_completada__isnull=True)

    return render(request, 'tareas.html', {
        'tareas': actividades,
        'perfil': perfil,
        'titulo': 'Mi Rutina 💪'
    })


@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm()
        })

    user = authenticate(
        request,
        username=request.POST['username'],
        password=request.POST['password']
    )

    if user is None:
        return render(request, 'signin.html', {
            'form': AuthenticationForm(),
            'error': 'Usuario o contraseña incorrectos'
        })

    login(request, user)
    return redirect('tareas')

@login_required
@login_required
def crear_tareas(request):
    if request.method == 'GET':
        return render(request, "crear_tareas.html", {
            'form': CreatForm()
        })

    form = CreatForm(request.POST)

    if form.is_valid():
        nueva_tarea = form.save(commit=False)
        nueva_tarea.user = request.user
        nueva_tarea.save()
        return redirect('tareas')

    return render(request, "crear_tareas.html", {
        'form': form,
        'error': 'Datos inválidos'
    })

@login_required
@login_required
def detalle_tarea(request, task_id):
    tarea = get_object_or_404(Actividad, pk=task_id, user=request.user)

    if request.method == 'GET':
        form = CreatForm(instance=tarea)
        return render(request, 'detalles_tareas.html', {
            'actividad': tarea,
            'form': form
        })

    form = CreatForm(request.POST, instance=tarea)

    if form.is_valid():
        form.save()
        return redirect('tareas')

    return render(request, 'detalles_tareas.html', {
        'actividad': tarea,
        'form': form,
        'error': 'Error al actualizar'
    })
        
@login_required
@login_required
def completar(request, task_id):
    tarea = get_object_or_404(Actividad, pk=task_id, user=request.user)

    if request.method == 'POST':
        tarea.f_completada = timezone.now()
        tarea.save()

    return redirect('tareas')
    
@login_required   
@login_required
def eliminar(request, task_id):
    tarea = get_object_or_404(Actividad, pk=task_id, user=request.user)

    if request.method == 'POST':
        tarea.delete()

    return redirect('tareas')
@login_required
@login_required
@login_required
def tareas_completadas(request):
    actividades = Actividad.objects.filter(
        user=request.user,
        f_completada__isnull=False
    ).order_by('-f_completada')

    return render(request, 'tareas.html', {
        'tareas': actividades,
        'titulo': 'Tareas Completadas'
    })