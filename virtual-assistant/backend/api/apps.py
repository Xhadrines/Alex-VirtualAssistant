from django.apps import AppConfig

class ApiConfig(AppConfig):
    # Seteaza tipul de camp auto-generat pentru ID ca fiind BigAutoField
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Defineste numele aplicatiei ca 'api'
    name = 'api'
