from pathlib import Path

# Obtine directorul de baza al proiectului
BASE_DIR = Path(__file__).resolve().parent.parent

# Cheia secreta pentru protectia aplicatiei Django
SECRET_KEY = 'django-insecure-%u_6ly-$^@p#v(rl1s%2x&-v=_7v@8&=v9(e%w1%ls)n)bxxgy'

# Seteaza aplicatia in modul de dezvoltare
DEBUG = True

# Specifica domeniile permise pentru aplicatie
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Aplicatiile instalate in Django (incluzand aplicatia proprie 'api' si rest_framework)
INSTALLED_APPS = [
    'django.contrib.admin',  # Admin panel Django
    'django.contrib.auth',  # Autentificare utilizator
    'django.contrib.contenttypes',  # Tipuri de continut pentru model
    'django.contrib.sessions',  # Gestionarea sesiunilor utilizatorului
    'django.contrib.messages',  # Mesaje catre utilizatori
    'django.contrib.staticfiles',  # Fisiere statice (CSS, JS)
    'api.apps.ApiConfig',  # Aplicatia personalizata 'api'
    'rest_framework',  # Suport pentru API-uri RESTful
    'corsheaders',  # Suport pentru CORS
]

# Middleware-ul care proceseaza fiecare cerere si raspuns
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Securitate aplicatie
    'django.contrib.sessions.middleware.SessionMiddleware',  # Gazduieste sesiuni
    'django.middleware.common.CommonMiddleware',  # Operatiuni comune pentru fiecare cerere
    'django.middleware.csrf.CsrfViewMiddleware',  # Protectie CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Autentificare utilizator
    'django.contrib.messages.middleware.MessageMiddleware',  # Mesaje pentru utilizatori
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Protectie clickjacking
    'corsheaders.middleware.CorsMiddleware',  # Suport CORS
    'django.middleware.common.CommonMiddleware',  # Middleware suplimentar pentru operatiuni comune
]

# Fisierul principal al URL-urilor
ROOT_URLCONF = 'backend.urls'

# Configurarea template-urilor pentru aplicatia Django
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Backend-ul pentru template-uri
        'DIRS': [],  # Director pentru template-uri (nu este setat aici)
        'APP_DIRS': True,  # Permite cautarea template-urilor in directoarele aplicatiilor
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Procesor de context pentru debug
                'django.template.context_processors.request',  # Procesor de context pentru cereri
                'django.contrib.auth.context_processors.auth',  # Procesor de context pentru autentificare
                'django.contrib.messages.context_processors.messages',  # Procesor de context pentru mesaje
            ],
        },
    },
]

# Aplicatia WSGI pentru serverul de productie
WSGI_APPLICATION = 'backend.wsgi.application'

# Configurarea bazei de date (folosind SQLite pentru dezvoltare)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Foloseste SQLite
        'NAME': BASE_DIR / 'db.sqlite3',  # Calea catre fisierul bazei de date
    }
}

# Validatori de parole pentru utilizatori
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Verifica similitudinea atributelor utilizatorului
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Minimul de caractere pentru parola
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Verifica parolele comune
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Verifica parolele numerice
    },
]

# Setarile de limba pentru aplicatie
LANGUAGE_CODE = 'en-us'

# Seteaza fusul orar
TIME_ZONE = 'UTC'

# Permite internazionalizarea aplicatiei
USE_I18N = True

# Permite utilizarea fusurilor orare
USE_TZ = True

# Calea pentru fisierele statice (CSS, JS, imagini)
STATIC_URL = 'static/'

# Seteaza tipul de camp automat pentru modelele Django
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Setarile CORS (permite doar accesul din domeniul local)
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:2002",  # Permite accesul doar de pe acest domeniu
]
