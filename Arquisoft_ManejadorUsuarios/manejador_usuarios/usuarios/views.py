from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario, Institucion
from django.contrib.auth.models import User
import json

@csrf_exempt
def crear_usuario(request):
    if request.method == 'POST':
        try:
            # Verifica si los datos vienen de un formulario (POST clásico) o en formato JSON
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            institucion = Institucion.objects.get(id=data['institucion_id'])

            # Crear el usuario
            usuario = Usuario.objects.create(
                usuario=data['usuario'],
                correo=data['correo'],
                nombre=data['nombre'],
                contrasenia=data['contrasenia'],
                rol=data['rol'],
                institucion= institucion
            )

            user = User.objects.create_user(data['usuario'], data['correo'], data['contrasenia'])
            user.first_name = data['rol']; 
            user.last_name = institucion.nombre; 
            user.save()
            
            return JsonResponse({"mensaje": "Usuario creado con exito", "usuario_id": usuario.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)

def formulario_usuario(request):
    return render(request, 'formulario_usuario.html')

def listar_usuarios(request, usuario_id=None):
    if request.method == 'GET':
        if usuario_id:
            usuario = Usuario.objects.filter(id=usuario_id).values('id', 'usuario', 'correo', 'nombre', 'rol', 'institucion__nombre')
            if usuario.exists():
                return JsonResponse(list(usuario), safe=False)
            else:
                return JsonResponse({"error": "Usuario no encontrado"}, status=404)
        else:
            usuarios = Usuario.objects.all().values('id', 'usuario', 'correo', 'nombre', 'rol', 'institucion__nombre')
            return JsonResponse(list(usuarios), safe=False)
    return JsonResponse({"error": "Método no permitido"}, status=405)

def pagina_inicio(request):
    return render(request, 'inicio.html')

def pagina_principal_usuarios(request):
    return render(request, 'usuarios_principal.html')
