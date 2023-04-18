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
        nombre_producto = cleaned_data.get('nombre_producto')
        codigo_producto = cleaned_data.get('codigo_producto')

        # por si quiere agregar un mensaje adicional     
        # if not nombre_producto:
        #     self.add_error('nombre_producto', 'El campo Nombre de Producto es requerido.')
        # elif not codigo_producto:
        #     self.add_error('codigo_producto', 'El campo Código de Producto es requerido.')

        if nombre_producto and codigo_producto:
            cleaned_data['nombre_producto'] = nombre_producto.upper()
            cleaned_data['codigo_producto'] = codigo_producto.upper()

        return cleaned_data