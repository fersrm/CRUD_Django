from django.contrib import admin
from ProyecBazarApp.models import *
#Register your models here.

admin.site.register(Rol)
admin.site.register(Comuna)
admin.site.register(Region)
admin.site.register(Marca)
admin.site.register(Categoria)
admin.site.register(TipoGiro)

#-----------------USUARIO------------------------------------------------------------------------------------------------
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.admin import UserAdmin

#para el formulario de creacion de usuarios
class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'rol_FK')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
    
        return password2

# esto es el formulario para editar el usuario
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm # Utiliza el nuevo formulario personalizado
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'rol_FK'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'rol_FK')}),
        ('Informacion', {'fields': ('username', 'password',)}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
    #    ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    # lo que se muestra al listar usuarios
    list_display = ('username', 'first_name', 'last_name','email', 'rol_FK','is_staff')

admin.site.register(Usuario, CustomUserAdmin)

#------------------FACTURAS-BOLETAS------------------------------------------------------------------------------------------------
def generate_admin(model, user_field_name):
    class CustomAdmin(admin.ModelAdmin):
        readonly_fields = ('fecha_emision',)

        def vendedor(self, obj):
            return getattr(obj, user_field_name)

        vendedor.short_description = 'Vendedor'

        id_field = 'id_boleta' if hasattr(model, 'id_boleta') else 'id_factura'
        list_display = (id_field, 'fecha_emision', 'total_factura' if hasattr(model, 'total_factura') else 'total_boleta', 'vendedor')

    return CustomAdmin

admin.site.register(Facturas, generate_admin(Facturas, 'usuario_FK'))
admin.site.register(Boletas, generate_admin(Boletas, 'usuario_FK'))

#-----------------PRODUCTOS------------------------------------------------------------------------------------------------------
class ProducAdmin(admin.ModelAdmin):
    readonly_fields = ('usuario_FK',)

    def marca(self, obj):
            return getattr(obj, 'marca_FK')

    marca.short_description = 'Marca'
     
    def categoria(self, obj):
            return getattr(obj, 'categoria_FK')

    categoria.short_description = 'Categoria'

    list_display = ('id_producto', 'codigo_producto', 'nombre_producto','precio_producto', 'marca','categoria')

admin.site.register(Producto,ProducAdmin)

#-------------------------CLIENTE-----------------------------------------------------------------------------------------------
class ClienteAdmin(admin.ModelAdmin):

    def comuna(self, obj):
            return getattr(obj, 'comuna_FK')

    comuna.short_description = 'Comuna'
     
    list_display = ('id_cliente', 'run_cliente', 'nombre_cliente','apellido_cliente', 'comuna')

admin.site.register(Cliente,ClienteAdmin)
#-------------------------------DATOS-EMPRESA------------------------------------------------------------------------------------
class EmpresaAdmin(admin.ModelAdmin):
     
    list_display = ('id_datos_empresa','nombre_empresa','estado')

admin.site.register(DatosEmpresa,EmpresaAdmin)
