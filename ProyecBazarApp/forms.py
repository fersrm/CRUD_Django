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
    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['codigo_producto'] = cleaned_data['codigo_producto'].upper()
        cleaned_data['nombre_producto'] = cleaned_data['nombre_producto'].upper()
        return cleaned_data
