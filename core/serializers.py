from rest_framework import serializers
from .models import Event, Registration, EventReport
from django.contrib.auth.models import User

# Serializers convertem os modelos do banco de dados para o formato JSON (e vice-versa)

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer básico para informações do usuário.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class EventSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo de Evento.
    """
    organizer = UserSerializer(read_only=True)
    
    class Meta:
        model = Event
        fields = ['id', 'organizer', 'title', 'description', 'event_date', 'location']
        # O campo 'location' será serializado usando GeoJSON graças ao DRF-GIS

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo de Inscrição.
    """
    volunteer = UserSerializer(read_only=True)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = Registration
        fields = ['id', 'volunteer', 'event', 'registered_at']

class EventReportSerializer(serializers.ModelSerializer):
    """
    Serializer para os Relatórios pós-ação.
    """
    author = UserSerializer(read_only=True)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    
    class Meta:
        model = EventReport
        fields = ['id', 'event', 'author', 'content', 'photo_url', 'created_at']