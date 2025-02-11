from rest_framework import serializers
from .models import ConversationHistory

# Definirea serializer-ului pentru modelul ConversationHistory
class ConversationHistorySerializer(serializers.ModelSerializer):
    
    # Definirea metadatelor pentru serializer
    class Meta:
        model = ConversationHistory  # Specifica modelul care va fi serializat
        fields = ('id', 'question', 'answer', 'created_at')  # Specifica campurile care vor fi incluse in serializare
