# Librerías de Django
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

# Modelos y formularios
from .forms import ProductoForm
from .models import Producto, Facturas, Boletas

# Librerías para generar PDF
import os
import pdfkit
import tempfile
import webbrowser

# Create your views here.
@login_required(login_url='/login/')
def home(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardar el nuevo producto en la base de datos
            form.clean() #transforma a mayuscula
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
    # Renderizado de la plantilla
    context = {'form': form, 'error_message': error_message}
    return render(request, 'ProyecBazarApp/home.html', context)

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
    # Renderizado de la plantilla   
    context = {"productos":productos}
    return render(request,"ProyecBazarApp/tienda.html",context)

#-------------------------------------------cambiar por Factura mas adelante ------------------------------------
@login_required(login_url='/login/')
def pagos(request):
    # Búsqueda de productos
    busqueda = request.GET.get('buscar')
    productos = Producto.objects.all()
    if busqueda:
        productos = Producto.objects.filter(
            Q(nombre_producto__icontains=busqueda) |
            Q(codigo_producto__icontains=busqueda) |
            Q(marca_FK__nombre_marca__icontains=busqueda) |
            Q(categoria_FK__nombre_categoria__icontains=busqueda)
        ).distinct()
    # Paginación de resultados
    paginator = Paginator(productos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Generación de PDF
    producPDF = productos
    # si se envía un formulario con el botón "Generar PDF", se genera la vista previa del PDF
    if request.method == 'POST' and 'generar_pdf' in request.POST:
        # generar el contenido HTML
        with open('ProyecBazarApp/templates/ProyecBazarApp/include/plantilla.html', 'r') as f:
            html_content = f.read()

        # añadir los datos de la tabla al contenido HTML
        html_content += '<table>'
        html_content += '<thead><tr><th>Código</th><th>Nombre</th><th>Precio</th><th>Marca</th><th>Categoría</th></tr></thead><tbody>'
        for producto in producPDF:
            html_content += f'<tr><td>{producto.codigo_producto}</td><td>{producto.nombre_producto}</td><td>{producto.precio_producto}</td><td>{producto.marca_FK}</td><td>{producto.categoria_FK}</td></tr>'
        html_content += '</tbody></table>'

        # Guardar el contenido HTML en un archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_file:
            tmp_file.write(html_content.encode('utf-8'))
            tmp_file.flush()

            # Generar el PDF a partir del contenido del archivo temporal
            pdf_content = pdfkit.from_file(tmp_file.name, False)

            # Guardamos el contenido del PDF en un archivo temporal
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_file:
                pdf_file.write(pdf_content)
                pdf_file.flush()

                # Abrimos la vista previa del PDF en el navegador
                webbrowser.open_new_tab(pdf_file.name)

        # Cerrar manualmente el archivo temporal
        os.unlink(tmp_file.name)

    return render(request, 'ProyecBazarApp/pagos.html', {'page_obj': page_obj})

#-----------------------------------------------------------------------------------------------------------------------
def salir(request):
    logout(request)
    return redirect('/')


#-----------------------------------------------------------------
@login_required(login_url='/login/')
def vita_facturas(request):
    # Búsqueda de facturas
    busqueda = request.GET.get('buscar')
    facturas = Facturas.objects.all()
    if busqueda:
        facturas = Facturas.objects.filter(
            Q(id_factura=busqueda) |
        #    Q(fecha_emision=busqueda) |
            Q(total_factura=busqueda) |
            Q(usuario_FK__username=busqueda) 
        ).distinct()
    # Paginación de resultados
    paginator = Paginator(facturas, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Generación de PDF
    facturaPDF = facturas
    # si se envía un formulario con el botón "Generar PDF", se genera la vista previa del PDF
    if request.method == 'POST' and 'informeFacturas_pdf' in request.POST:
        # generar el contenido HTML
        with open('ProyecBazarApp/templates/ProyecBazarApp/include/plantilla.html', 'r') as f:
            html_content = f.read()

        # añadir los datos de la tabla al contenido HTML
        html_content += '<table>'
        html_content += '<thead><tr><th>Folio</th><th>Total</th><th>Vendedor</th><th>Fecha de emisión</th></tr></thead><tbody>'
        for factura in facturaPDF:
            html_content += f'<tr><td>{factura.id_factura}</td><td>{factura.total_factura}</td><td>{factura.usuario_FK}</td><td>{factura.fecha_emision.date()}</td></tr>'
        html_content += '</tbody></table>'

        # Guardar el contenido HTML en un archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_file:
            tmp_file.write(html_content.encode('utf-8'))
            tmp_file.flush()

            # Generar el PDF a partir del contenido del archivo temporal
            pdf_content = pdfkit.from_file(tmp_file.name, False)

            # Guardamos el contenido del PDF en un archivo temporal
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_file:
                pdf_file.write(pdf_content)
                pdf_file.flush()

                # Abrimos la vista previa del PDF en el navegador
                webbrowser.open_new_tab(pdf_file.name)

        # Cerrar manualmente el archivo temporal
        os.unlink(tmp_file.name)

    return render(request, 'ProyecBazarApp/informeFactura.html', {'page_obj': page_obj})
#-----------------------------------------boletas---------------------------------------------------------------------------------------
@login_required(login_url='/login/')
def vita_boletas(request):
    # Búsqueda de boletas
    busqueda = request.GET.get('buscar')
    boletas = Boletas.objects.all()
    if busqueda:
        boletas = Boletas.objects.filter(
            Q(id_boleta=busqueda) |
        #    Q(fecha_emision=busqueda) |
            Q(total_boleta=busqueda) |
            Q(usuario_FK__username=busqueda) 
        ).distinct()
    # Paginación de resultados
    paginator = Paginator(boletas, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Generación de PDF
    BoletasPDF = boletas
    # si se envía un formulario con el botón "Generar PDF", se genera la vista previa del PDF
    if request.method == 'POST' and 'informeBoletas_pdf' in request.POST:
        # generar el contenido HTML
        with open('ProyecBazarApp/templates/ProyecBazarApp/include/plantilla.html', 'r') as f:
            html_content = f.read()

        # añadir los datos de la tabla al contenido HTML
        html_content += '<table>'
        html_content += '<thead><tr><th>Folio</th><th>Total</th><th>Vendedor</th><th>Fecha de emisión</th></tr></thead><tbody>'
        for boleta in BoletasPDF:
            html_content += f'<tr><td>{boleta.id_boleta}</td><td>{boleta.total_boleta}</td><td>{boleta.usuario_FK}</td><td>{boleta.fecha_emision.date()}</td></tr>'
        html_content += '</tbody></table>'

        # Guardar el contenido HTML en un archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_file:
            tmp_file.write(html_content.encode('utf-8'))
            tmp_file.flush()

            # Generar el PDF a partir del contenido del archivo temporal
            pdf_content = pdfkit.from_file(tmp_file.name, False)

            # Guardamos el contenido del PDF en un archivo temporal
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_file:
                pdf_file.write(pdf_content)
                pdf_file.flush()

                # Abrimos la vista previa del PDF en el navegador
                webbrowser.open_new_tab(pdf_file.name)

        # Cerrar manualmente el archivo temporal
        os.unlink(tmp_file.name)

    return render(request, 'ProyecBazarApp/informeBoleta.html', {'page_obj': page_obj})