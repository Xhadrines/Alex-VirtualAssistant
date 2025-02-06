from django.apps import AppConfig  # Importa clasa AppConfig din Django

class ApiConfig(AppConfig):
    """
    Configuratia aplicatiei 'api'. Aceasta este utilizata pentru setarile specifice aplicatiei
    si pentru a integra aplicatia in cadrul proiectului.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Seteaza campul auto-incrementabil implicit pentru modelele Django la BigAutoField

    name = 'api'  # Numele aplicatiei, care va fi utilizat pentru integrarea acesteia in proiectul Django
