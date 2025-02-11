import os
from django.core.wsgi import get_wsgi_application

# Seteaza variabila de mediu pentru configuratiile Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Creeaza aplicatia WSGI pentru a rula proiectul Django
application = get_wsgi_application()
