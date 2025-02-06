from django.urls import path  # Importa functia path din django.urls
from .views import home, chat_llama, ConversationHistoryView  # Importa functiile si clasele view asociate rutelelor

# Listeaza rutele URL ale aplicatiei
urlpatterns = [
    path('', home, name="home"),  # Ruta pentru pagina principala, asociaza functia 'home' view-ului
    path('chat/', chat_llama, name='chat_llama'),  # Ruta pentru chat, asociaza functia 'chat_llama' view-ului
    path('history/', ConversationHistoryView.as_view(), name='conversation_history'),  # Ruta pentru istoricul conversatiilor, asociaza 'ConversationHistoryView' view-ului, utilizand 'as_view()' pentru a crea o instanta a clasei
]
