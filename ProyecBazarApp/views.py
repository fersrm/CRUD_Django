from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .models import Producto
from django.db.models import Q
from .forms import ProductoForm

# Create your views here.
@login_required(login_url='/login/')
def home(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardar el nuevo producto en la base de datos
            form.save()
            # Redireccionar al usuario a otra página
            return redirect('Tienda')
    else:
        form = ProductoForm()

      # Aquí agregamos el mensaje de error en caso de que el formulario no sea válido
    if not form.is_valid():
        error_message = form.errors
    else:
        error_message = "valido"

    return render(request, 'ProyecBazarApp/home.html', {'form': form, 'error_message': error_message})

@login_required(login_url='/login/')
def tienda(request):
    busqueda = request.GET.get('buscar')
    productos = Producto.objects.all()

    if busqueda:
        productos = Producto.objects.filter(
            Q(nombre_producto__icontains = busqueda) |
            Q(codigo_producto__icontains = busqueda) |
            Q(marca_FK__nombre_marca__icontains = busqueda) |
            Q(categoria_FK__nombre_categoria__icontains = busqueda) 
        ).distinct()
    context = {"productos":productos}
    return render(request,"ProyecBazarApp/tienda.html",context)

@login_required(login_url='/login/')
def pagos(request):
    return render(request,"ProyecBazarApp/pagos.html")

def salir(request):
    logout(request)
    return redirect('/')
