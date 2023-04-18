from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo_producto', 'nombre_producto','precio_producto','imagen','marca_FK','categoria_FK']
        labels = {
            'marca_FK': 'Marca',
            'categoria_FK': 'Categoria'
        }
