"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin  # Importa modulul admin pentru a accesa zona de administrare Django
from django.urls import path, include  # Importa functiile path si include pentru a defini rutele URL si a include alte fisiere de configurare URL
from api.views import home  # Importa functia home din fisierul de views al aplicatiei 'api'

# Lista principala de rute URL ale aplicatiei
urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta pentru interfata de administrare Django
    path('', home, name='home'),  # Ruta pentru pagina principala, care va utiliza functia home din views
    path('api/', include('api.urls')),  # Include rutele definite in fisierul 'api.urls', pentru a organiza rutele API-ului
]
