from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Event, Registration, EventReport
from .serializers import EventSerializer, RegistrationSerializer, EventReportSerializer

# Importações de Geoprocessamento (PostGIS)
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D  # 'D' é para Distância

class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint para criar, ler, atualizar e deletar Eventos.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # Todos podem ver, só autenticados podem criar/editar

    def perform_create(self, serializer):
        # Associa o organizador ao usuário logado
        serializer.save(organizer=self.request.user)

    # Este é o "Microserviço de Geoprocessamento" (simulado dentro do monólito)
    @action(detail=False, methods=['get'], permission_classes=[])
    def near_me(self, request):
        """
        Retorna eventos próximos a um ponto (lat/lon).
        Exemplo de chamada: /api/events/near_me/?lat=-23.55&lon=-46.63&dist=10
        """
        try:
            lat = float(request.query_params.get('lat'))
            lon = float(request.query_params.get('lon'))
            distance_km = float(request.query_params.get('dist', 10)) # Padrão de 10km
        except (TypeError, ValueError):
            return Response({"error": "Parâmetros 'lat', 'lon' (float) são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        user_location = Point(lon, lat, srid=4326)
        
        # Filtro do PostGIS: location__distance_lte
        # Filtra eventos cuja localização (ponto) esteja a uma distância
        # menor ou igual (lte) à localização do usuário.
        queryset = Event.objects.filter(
            location__distance_lte=(user_location, D(km=distance_km))
        )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RegistrationViewSet(viewsets.ModelViewSet):
    """
    API endpoint para voluntários se inscreverem em eventos.
    """
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated] # Apenas logados podem se inscrever

    def get_queryset(self):
        # Retorna apenas as inscrições do usuário logado
        return Registration.objects.filter(volunteer=self.request.user)

    def perform_create(self, serializer):
        # Associa o voluntário ao usuário logado
        serializer.save(volunteer=self.request.user)

class EventReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint para relatórios pós-ação.
    """
    queryset = EventReport.objects.all()
    serializer_class = EventReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtra relatórios por evento (se o ID do evento for passado na URL)
        if 'event_pk' in self.kwargs:
            return EventReport.objects.filter(event_id=self.kwargs['event_pk'])
        return super().get_queryset()
    
    def perform_create(self, serializer):
        # Associa o autor ao usuário logado
        serializer.save(author=self.request.user)