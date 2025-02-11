from django.urls import path
from .views import home, chat_llama, ConversationHistoryView

urlpatterns = [
    path('', home, name="home"),  # Rutele pentru pagina principala
    path('chat/', chat_llama, name='chat_llama'),  # Rutele pentru chat
    path('history/', ConversationHistoryView.as_view(), name='conversation_history'),  # Rutele pentru istoricul conversatiilor
]
