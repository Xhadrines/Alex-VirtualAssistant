from rest_framework import serializers  # Importa modulul serializers din Django REST Framework
from .models import ConversationHistory  # Importa modelul ConversationHistory definit in fisierul models.py

class ConversationHistorySerializer(serializers.ModelSerializer):
    """
    Serializer pentru modelul ConversationHistory.
    Acesta va transforma obiectele modelului ConversationHistory in date JSON
    si invers, astfel incat sa poata fi utilizate in API-ul REST.
    """
    class Meta:
        model = ConversationHistory  # Specifica modelul pentru care se creeaza serializerul
        fields = ('id', 'question', 'answer', 'created_at')  # Listeaza campurile care vor fi incluse in serializare
