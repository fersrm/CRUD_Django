from django.urls import path
from django.contrib.auth.views import LoginView
from ProyecBazarApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', LoginView.as_view(template_name='ProyecBazarApp/login.html'), name='login'),
    path('', views.HomeView.as_view(), name='Home'),
    path('tienda/', views.TiendaView.as_view(), name='Tienda'),
    path('pagos/', views.PagosListView.as_view(), name='Pagos'),
    path('informe_facturas/', views.FacturaListView.as_view(), name='Facturas'),
    path('informe_Boletas/', views.BoletaListView.as_view(), name='Boletas'),
    path('salir/', views.SalirView.as_view(), name='salir'),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


