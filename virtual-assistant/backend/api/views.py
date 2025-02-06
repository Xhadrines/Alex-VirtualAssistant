from django.shortcuts import render  # Importa functia render din Django pentru a returna template-uri HTML
from rest_framework import generics  # Importa modulele necesare pentru a crea vizualizari bazate pe clase folosind Django REST Framework
from rest_framework.response import Response  # Importa Response, care este utilizat pentru a trimite raspunsuri HTTP din API-uri
from rest_framework.decorators import api_view  # Importa decoratori pentru a crea vizualizari API
import ollama  # Importa biblioteca 'ollama', care este utilizata pentru interactiunea cu modelul Llama
from .serializers import ConversationHistorySerializer  # Importa serializer-ul pentru modelul ConversationHistory
from .models import ConversationHistory  # Importa modelul ConversationHistory din baza de date

def ask_llama(question):
    """
    Trimite intrebarea la modelul Llama3.1 prin Ollama si returneaza raspunsul.
    Daca apare o eroare, returneaza un mesaj de eroare.
    """
    try:
        messages = [
            {"role": "system", "content": "Te rog sa raspunzi in limba romana."},  # Mesajul pentru a instrui modelul sa raspunda in limba romana
            {"role": "user", "content": question}  # Mesajul utilizatorului (intrebarea)
        ]
        # Rulam modelul Llama3.1 folosind Ollama
        response = ollama.chat(model="llama3.1", messages=messages)
        return response['message']['content']  # Extrage si returneaza raspunsul de la model
    except Exception as e:
        return f"Error: {str(e)}"  # Daca apare o eroare, returneaza mesajul de eroare

@api_view(['POST'])  # Decorator pentru a specifica ca aceasta functie raspunde doar la cereri POST
def chat_llama(request):
    """
    Vizualizarea care primeste o intrebare prin API, trimite intrebarea la modelul Llama,
    salveaza intrebarea si raspunsul in baza de date, si returneaza raspunsul.
    """
    try:
        question = request.data.get('message')  # Citim textul din cererea POST (in acest caz 'message')

        if not question:
            return Response("Eroare: Mesajul nu poate fi gol", status=400)  # Verificam daca intrebarea nu este goala

        answer = ask_llama(question)  # Obtinem raspunsul de la modelul Llama

        # Salvam conversatia in baza de date
        ConversationHistory.objects.create(question=question, answer=answer)

        return Response({
            # "question": question,  # Optional: putem returna intrebarea in raspuns
            "answer": answer  # Returneaza raspunsul generat de model
        })
    except Exception as e:
        return Response(f"Eroare interna: {str(e)}", status=500)  # Daca apare o eroare, returneaza un raspuns de eroare

class ConversationHistoryView(generics.ListAPIView):
    """
    Vizualizare care returneaza istoricul conversatiilor din baza de date.
    Utilizeaza serializer-ul ConversationHistorySerializer pentru a structura datele.
    """
    queryset = ConversationHistory.objects.all()  # Selecteaza toate inregistrarile din tabelul ConversationHistory
    serializer_class = ConversationHistorySerializer  # Foloseste serializer-ul pentru a transforma obiectele in JSON

def home(request):
    """
    Vizualizarea pentru pagina principala care afiseaza o lista de endpointuri.
    """
    endpoints = [
        {"name": "Chat Llama", "url": "/api/chat/"},  # Endpoint pentru chat
        {"name": "History", "url": "/api/history/"},  # Endpoint pentru istoricul conversatiilor
        {"name": "Admin", "url": "/admin/"},  # Endpoint pentru pagina admin
    ]
    return render(request, "home.html", {"endpoints": endpoints})  # Returneaza template-ul home.html cu lista de endpointuri
