import os
import sys

def main():
    # Seteaza variabila de mediu pentru configurarile Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    
    try:
        # Importa functia care va executa comenzile Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Daca Django nu e gasit, arunca o eroare clara
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Daca nu se dau argumente sau este specificat 'runserver', seteaza adresa si portul
    if len(sys.argv) == 1 or sys.argv[1] == "runserver":
        sys.argv = ["manage.py", "runserver", "127.0.0.1:2307"]

    # Executa comanda Django data in linia de comanda
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()  # Apelarea functiei principale daca fisierul este rulat direct
