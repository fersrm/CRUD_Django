# Librerías de Django
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect

# Modelos y formularios
from .forms import ProductoForm, DatosEmpresaForm, ProductoFormEditar
from .models import Producto, Facturas, Boletas, DatosEmpresa,DetalleFacturas

# Para trabajar con clases
from django.contrib.auth.views import LogoutView
from django.views.generic import ListView , UpdateView,DetailView,DeleteView,CreateView
from django.urls import reverse_lazy

# otras librerias
import glob
import os

# imporat funciones
from ProyecBazarApp import funcionesViews 

# Create your views here.---------------------------------------------------

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class HomeView(UpdateView,DetailView):
    model = DatosEmpresa
    form_class = DatosEmpresaForm
    template_name = 'ProyecBazarApp/home.html'
    success_url = reverse_lazy('Home')

    def get_object(self):
        return self.model.objects.get(pk=1)
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request,"Dia actualizado Correctamente")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Facturas -----------------------------
        facturas_data = funcionesViews.total_dia(Facturas,'cantidad_facturas', 'total_factura')
        context.update(facturas_data)
        # Boletas ---------------------------------
        boletas_data = funcionesViews.total_dia(Boletas,'cantidad_boletas', 'total_boleta') # total_boleta es el nombre del campo en la BBDD
        context.update(boletas_data)
        return context

#---------------------------TIENDA----CRUD------------------------------------------------------------

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ListarProductoView(ListView):
    model = Producto
    template_name = 'ProyecBazarApp/tienda.html'
    paginate_by = 2

    def get_queryset(self):
        busqueda = self.request.GET.get('buscar')
        campos_busqueda = ['nombre_producto', 'codigo_producto', 'marca_FK__nombre_marca','categoria_FK__nombre_categoria']
        return funcionesViews.buscar_campos(self.model, campos_busqueda, busqueda)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginate_by)
        page = self.request.GET.get('page')
        context['object_list'] = paginator.get_page(page)
        return context
#--------------------------------------------------------
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class AgregarProductoView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'ProyecBazarApp/modal/AddTienda.html'

    def form_valid(self, form):
        form.clean()
        form.save()
        messages.success(self.request, "Producto agregado correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error en el formulario')
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('Tienda')
#-----------------------------------------------------------------------
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class EditarProductoView(UpdateView):
    model = Producto
    form_class = ProductoFormEditar
    template_name = 'ProyecBazarApp/modal/tienda_edit.html'

    def form_valid(self, form):
        form.clean()
        form.save()
        messages.success(self.request, "Producto Editado correctamente")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error en el formulario')
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('Tienda')
#------------------------------------------------------------------------
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class EliminarProductoView(DeleteView):
    model = Producto
    success_url = reverse_lazy('Tienda')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        messages.success(self.request, "Producto eliminado correctamente")
        self.object.delete()
        return redirect(self.get_success_url())

#----------------------INFORMES-----------------------------------------------
#----------------------FACTURAS----------------------------------------------

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class FacturaListView(ListView):
    model = Facturas
    template_name = 'ProyecBazarApp/informeFactura.html'
    paginate_by = 10

    def get_queryset(self):
        busqueda = self.request.GET.get('buscar')
        busquedaF = self.request.GET.get('buscarFecha')
        campos_busqueda = ['id_factura', 'total_factura', 'usuario_FK__username']
        return funcionesViews.buscar_campos(self.model,campos_busqueda,busqueda,busquedaF)

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
            camposTH = ['Folio','Total','Vendedor','Fecha de emisión']
            camposTB = ['id_factura','total_factura','usuario_FK','fecha_emision']
            funcionesViews.generar_pdf_boletas(queryset,camposTH,camposTB)
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
        return funcionesViews.buscar_campos(self.model,campos_busqueda,busqueda,busquedaF)

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
            camposTH = ['Folio','Total','Vendedor','Fecha de emisión']
            camposTB = ['id_boleta','total_boleta','usuario_FK','fecha_emision']
            funcionesViews.generar_pdf_boletas(queryset,camposTH,camposTB)
        return self.get(self.request, *args, **kwargs)

#-------------------------------------------cambiar por Factura mas adelante ------------------------------------
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class PagosListView(ListView):
    model = DetalleFacturas
    template_name = 'ProyecBazarApp/pagos.html'

#-----------------------SALIR------------------------------------------------------------------------------------------------

class SalirView(LogoutView):
    next_page = '/'  
    def dispatch(self, request, *args, **kwargs):
        # Eliminar archivos temporales aquí
        pdf_file_path = 'C:/Users/HP/AppData/Local/Temp/*.pdf'
        html_file_path = 'C:/Users/HP/AppData/Local/Temp/*.html'   
        for file_path in glob.glob(pdf_file_path):
            os.remove(file_path)
        for file_path in glob.glob(html_file_path):
            os.remove(file_path)
        # Llamar al método dispatch() original
        return super().dispatch(request, *args, **kwargs)

        