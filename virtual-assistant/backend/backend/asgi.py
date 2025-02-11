import os
from django.core.asgi import get_asgi_application

# Seteaza variabila de mediu pentru configuratiile Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Creeaza aplicatia ASGI pentru a rula proiectul Django
application = get_asgi_application()
