from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .models import Producto
from django.db.models import Q

# Create your views here.
@login_required(login_url='/login/')
def home(request):
    return render(request,"ProyecBazarApp/home.html")

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




