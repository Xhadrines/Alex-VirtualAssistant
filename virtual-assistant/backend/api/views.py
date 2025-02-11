from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
import ollama
from .serializers import ConversationHistorySerializer
from .models import ConversationHistory

def ask_llama(question):
    try:
        # Configuram mesajele pentru interactiunea cu Llama
        messages = [
            {"role": "system", "content": "Te rog sa raspunzi in limba romana, pe tine te cheama 'Alex' si esti asistentul virtual pentru 'Facultatea de Inginerie Electrica si Stiinta Calculatoarelor'."},
            {"role": "user", "content": question}
        ]
        response = ollama.chat(model="llama3.1", messages=messages)  # Trimitem intrebarea si obtinem raspunsul de la Llama
        return response['message']['content']  # Returneaza raspunsul generat
    except Exception as e:
        return f"Error: {str(e)}"  # Returneaza eroare in caz de exceptie

@api_view(['POST'])  # Defineste un endpoint API POST pentru chat
def chat_llama(request):
    try:
        question = request.data.get('message')  # Extrage intrebarea din cererea API

        if not question:  # Verifica daca intrebarea este goala
            return Response("Eroare: Mesajul nu poate fi gol", status=400)

        answer = ask_llama(question)  # Obtine raspunsul de la Llama

        # Creeaza un obiect de tip ConversationHistory pentru a salva intrebarea si raspunsul
        ConversationHistory.objects.create(question=question, answer=answer)

        return Response({
            "answer": answer  # Returneaza raspunsul ca un obiect JSON
        })
    except Exception as e:
        return Response(f"Eroare interna: {str(e)}", status=500)  # Returneaza eroare in caz de exceptie

class ConversationHistoryView(generics.ListAPIView):
    queryset = ConversationHistory.objects.all()  # Obtine toate obiectele ConversationHistory
    serializer_class = ConversationHistorySerializer  # Foloseste serializerul pentru a transforma obiectele in JSON

def home(request):
    # Definirea endpoint-urilor disponibile
    endpoints = [
        {"name": "Chat Llama", "url": "/api/chat/"},
        {"name": "History", "url": "/api/history/"},
        {"name": "Admin", "url": "/admin/"}
    ]
    return render(request, "home.html", {"endpoints": endpoints})  # Returneaza pagina home cu lista de endpoint-uri
