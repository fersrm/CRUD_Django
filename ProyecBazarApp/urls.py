from django.urls import path
from django.contrib.auth.views import LoginView
from ProyecBazarApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', LoginView.as_view(template_name='ProyecBazarApp/login.html'), name='login'),
    path('', views.home, name='Home'),
    path('tienda/', views.tienda, name='Tienda'),
    path('pagos/', views.pagos, name='Pagos'),
    path('salir/', views.salir, name='salir'),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


