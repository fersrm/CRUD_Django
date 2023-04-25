# Librerías para generar PDF
import pdfkit
import tempfile
import webbrowser
# para filtar
from django.utils import timezone
from django.db.models import Q,Sum
# modelos
from .models import Producto

def generar_pdf_boletas(queryset,camposH,camposB):
    # Plantilla HTML
    with open('ProyecBazarApp/templates/ProyecBazarApp/include/plantilla.html', 'r') as f:
        contenido = f.read()
    # Generar contenido HTML
    contenido += '<table>'
    contenido += '<thead><tr>'
    for campo in camposH: # Generar los th
        contenido += f'<th>{campo}</th>'
    contenido += '</tr></thead><tbody>'
    for obj in queryset: # Genera los tr
        contenido += '<tr>'
        for campo in camposB:
            if campo == 'fecha_emision':
                contenido += f'<td>{getattr(obj, campo).date()}</td>'
            else:
                contenido += f'<td>{getattr(obj, campo)}</td>'
        contenido += '</tr>'
    # Generar nombre único para el archivo temporal HTML
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp_html:
        tmp_html.write(contenido.encode('utf-8'))
        tmp_html.flush()
        # Generar PDF a partir del contenido del archivo temporal
        pdf_content = pdfkit.from_file(tmp_html.name, False)
        # Generar nombre único para el archivo temporal PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
            tmp_pdf.write(pdf_content)
            tmp_pdf.flush()
            # Abrir la vista previa del PDF en el navegador
            webbrowser.open_new_tab(tmp_pdf.name)


def buscar_campos(model, campos, busqueda, busquedaF=""):
    modelo = model.objects.all()
    if busqueda:
        if isinstance(model(), Producto): # Agregar los modelos aqui para busquedas no exactas
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

def total_dia(model, count_field, sum_field):
    today = timezone.now().date() #fecha actual
    query = Q(fecha_emision__icontains=today) 
    objects = model.objects.filter(query).distinct()
    count = objects.count()
    total = objects.aggregate(total=Sum(sum_field))['total']
    return {count_field: count, sum_field: total if total is not None else 0}
