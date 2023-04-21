# Librerías de Django
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.decorators import method_decorator

# Modelos y formularios
from .forms import ProductoForm
from .models import Producto, Facturas, Boletas

# Librerías para generar PDF
import os
import pdfkit
import tempfile
import webbrowser

# Para trabajar con clases
from django.contrib.auth.views import LogoutView
from django.views.generic import ListView , CreateView
from django.urls import reverse_lazy

# Nueva función para generar PDF
import os
import tempfile
import webbrowser

import pdfkit


def generar_pdf_boletas(queryset):
    # Plantilla HTML
    with open('ProyecBazarApp/templates/ProyecBazarApp/include/plantilla.html', 'r') as f:
        contenido = f.read()
    # Generar contenido HTML
    contenido += '<table>'
    contenido += '<thead><tr><th>Folio</th><th>Total</th><th>Vendedor</th><th>Fecha de emisión</th></tr></thead><tbody>'
    for objeto in queryset:
        contenido += f'<tr><td>{objeto.id_boleta}</td><td>{objeto.total_boleta}</td><td>{objeto.usuario_FK}</td><td>{objeto.fecha_emision.date()}</td></tr>'
    contenido += '</tbody></table>'
    # Guardar contenido HTML en un archivo temporal
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_file:
        tmp_file.write(contenido.encode('utf-8'))
        tmp_file.flush()
        # Generar PDF a partir del contenido del archivo temporal
        pdf_content = pdfkit.from_file(tmp_file.name, False)
        # Guardar contenido del PDF en un archivo temporal
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_file:
            pdf_file.write(pdf_content)
            pdf_file.flush()
            # Abrir la vista previa del PDF en el navegador
            webbrowser.open_new_tab(pdf_file.name)
        # Cerrar manualmente el archivo temporal
        os.unlink(tmp_file.name)

def buscar_campos(model, campos, busqueda, busquedaF=""):
    modelo = model.objects.all()
    if busqueda:
        if isinstance(model(), Producto):
            queries = [Q(**{campo + '__icontains': busqueda}) for campo in campos]
        else:
            try:
                int(busqueda)
            except ValueError:
                return model.objects.none()
            queries = [Q(**{campo: busqueda}) for campo in campos]
        query = queries.pop()
        for item in queries:
            query |= item
        modelo = modelo.filter(query).distinct()
    elif busquedaF:
        query = Q(fecha_emision__icontains=busquedaF) 
        modelo = modelo.filter(query).distinct()
    return modelo

# Create your views here.---------------------------------------------------

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class HomeCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'ProyecBazarApp/home.html'
    success_url = reverse_lazy('Tienda')

    def form_valid(self, form):
        form.clean() # transforma a mayúsculas
        return super().form_valid(form)

    def form_invalid(self, form):
        error_message = form.errors
        context = self.get_context_data(form=form, error_message=error_message)
        return self.render_to_response(context)

#---------------------------TIENDA-----------------------------------------------------------------

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TiendaListView(ListView):
    model = Producto
    template_name = 'ProyecBazarApp/tienda.html'
    paginate_by = 8

    def get_queryset(self):
        busqueda = self.request.GET.get('buscar')
        campos_busqueda = ['nombre_producto', 'codigo_producto', 'marca_FK__nombre_marca','categoria_FK__nombre_categoria']
        return buscar_campos(self.model,campos_busqueda,busqueda)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginate_by)
        page = self.request.GET.get('page')
        context['object_list'] = paginator.get_page(page)
        return context
    
#----------------------INFORMES-----------------------------------------------
#----------------------FACTURAS----------------------------------------------------------

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class FacturaListView(ListView):
    model = Facturas
    template_name = 'ProyecBazarApp/informeFactura.html'
    paginate_by = 10

    def get_queryset(self):
        busqueda = self.request.GET.get('buscar')
        busquedaF = self.request.GET.get('buscarFecha')
        campos_busqueda = ['id_factura', 'total_factura', 'usuario_FK__username']
        return buscar_campos(self.model,campos_busqueda,busqueda,busquedaF)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginate_by)
        page = self.request.GET.get('page')
        context['object_list'] = paginator.get_page(page)
        return context
    #--------------------PDF------------------------------------
    def post(self, *args, **kwargs):
        # Si se envió el formulario de generar PDF, se genera el PDF
        if self.request.method == 'POST' and 'informeFacturas_pdf' in self.request.POST:
            queryset = self.get_queryset()
            generar_pdf_boletas(queryset)
        return self.get(self.request, *args, **kwargs)
    
#-----------------------BOLETAS--------------------------------------------------------------------------------------

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class BoletaListView(ListView):
    model = Boletas
    template_name = 'ProyecBazarApp/informeBoleta.html'
    paginate_by = 10

    def get_queryset(self):
        busqueda = self.request.GET.get('buscar')
        busquedaF = self.request.GET.get('buscarFecha')
        campos_busqueda = ['id_boleta', 'total_boleta', 'usuario_FK__username']
        return buscar_campos(self.model,campos_busqueda,busqueda,busquedaF)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginate_by)
        page = self.request.GET.get('page')
        context['object_list'] = paginator.get_page(page)
        return context
    #--------------------PDF------------------------------------
    def post(self, *args, **kwargs):
        # Si se envió el formulario de generar PDF, se genera el PDF
        if self.request.method == 'POST' and 'informeBoletas_pdf' in self.request.POST:
            queryset = self.get_queryset()
            generar_pdf_boletas(queryset)
        return self.get(self.request, *args, **kwargs)

#-------------------------------------------cambiar por Factura mas adelante ------------------------------------
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class PagosListView(ListView):
    pass

#-----------------------SALIR------------------------------------------------------------------------------------------------

class SalirView(LogoutView):
    next_page = '/'
