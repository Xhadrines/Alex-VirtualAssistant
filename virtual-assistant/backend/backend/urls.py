from django.contrib import admin
from django.urls import path, include
from api.views import home

# Definirea URL-urilor aplicatiei
urlpatterns = [
    path('admin/', admin.site.urls),  # URL-ul pentru panelul de administrare Django
    path('', home, name='home'),  # URL-ul pentru pagina principala, care apeleaza functia 'home'
    path('api/', include('api.urls')),  # Include URL-urile din aplicatia 'api'
]
