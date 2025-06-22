# Backend

Aceasta este **partea de backend** a aplicației, construită folosind framework-ul **Django + Django REST framework**.

## Cerințe

Pentru a rula aplicația, trebuie să ai instalat:

- **Python** (v3.13.2 sau o versiune mai mare)
- **pip** (v24.3.1 sau o versiune mai mare)

## Instalare

1. Asigură-te că ai instalat gtk3-runtime de pe

```bash
https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases
```

2. Asigură-te că te afli în directorul `backend`

3. Creează un fișier `.env` și adaugă următoarea linie:

```bash
SENDGRID_API_KEY=[API_KEY_SENDGRID]
SENDGRID_FROM_EMAIL=[EMAIL_VALIT]
```

_Note: Înlocuiește `[API_KEY_SENDGRID]` și `[EMAIL_VALIT]` cu valorile corespunzătoare._

4. Creează mediul virtual folosind comanda:

```bash
python -m venv .venv
```

5. Activează mediul virtual folosind comanda:

```bash
.\.venv\Scripts\activate
```

6. Instalează dependențele folosind comanda:

```bash
pip install -r requirements.txt
```

7. Crează migrațiile folosind comanda:

```bash
python manage.py makemigrations
```

8. Aplică migrațiile folosind comanda:

```bash
python manage.py migrate
```

9. Instalează Ollama mergând pe [site-ul oficial Ollama](https://ollama.com/).

10. Instalează modelul Llama 3.2 folosind comanda:

```bash
ollama pull llama3.2
```

11. Rulează proiectul folosind comanda:

```bash
python manage.py runserver
```

12. Proiectul rulează pe `http://127.0.0.1:2307/`.
