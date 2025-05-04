from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Facultate, Specializare, Grupa, UserProfile, Adevetinta, ConversationHistory

# ----------------------------------------------------------------------------------------------------

class FacultateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facultate
        fields = ['nume']

# ----------------------------------------------------------------------------------------------------

class SpecializareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specializare
        fields = ['nume', 'facultate']

# ----------------------------------------------------------------------------------------------------

class GrupaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupa
        fields = ['an_universitar', 'an_studiu', 'grupa', 'semigrupa', 'facultate', 'specializare']

# ----------------------------------------------------------------------------------------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validate_data):
        user = User.objects.create_user(
            username=validate_data['username'],
            password=validate_data['password'],
            email=validate_data.get('email', ''),
            first_name=validate_data.get('first_name', ''),
            last_name=validate_data.get('last_name', ''),
        )
        return user

# ----------------------------------------------------------------------------------------------------

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'facultate', 'specializare', 'grupa', 'is_2fa_enable', 'totp_secret_key', 'totp_enable_at', 'is_2fa_verified']

# ----------------------------------------------------------------------------------------------------

class AdevetintaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adevetinta
        fields = ['user', 'last_name', 'first_name', 'an_universitar', 'an_studiu', 'specializare', 'motiv', 'data_emitere', 'numar', 'status', 'pdf_link', 'is_downloaded', 'expires_at']

# ----------------------------------------------------------------------------------------------------

class ConversationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationHistory
        fields = ['user', 'question', 'answer', 'date_create']

# ----------------------------------------------------------------------------------------------------
