from django.contrib.gis.db import models as gis_models  # Importa os modelos do GIS
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Event(models.Model):
    """
    Representa um evento/mutirão criado por um usuário.
    """
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organized_events", verbose_name=_("Organizador"))
    title = models.CharField(_("Título"), max_length=255)
    description = models.TextField(_("Descrição"))
    event_date = models.DateTimeField(_("Data do Evento"))
    
    # Campo de Geoprocessamento (PostGIS)
    # Armazena o ponto (Latitude/Longitude) do evento
    location = gis_models.PointField(_("Localização (Ponto)"), srid=4326) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Evento")
        verbose_name_plural = _("Eventos")

    def _str_(self):
        return self.title

class Registration(models.Model):
    """
    Representa a inscrição de um voluntário em um evento.
    """
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="registrations", verbose_name=_("Voluntário"))
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="participants", verbose_name=_("Evento"))
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Inscrição")
        verbose_name_plural = _("Inscrições")
        unique_together = ('volunteer', 'event') # Garante que um usuário só se inscreva uma vez

    def _str_(self):
        return f"{self.volunteer.username} @ {self.event.title}"

class EventReport(models.Model):
    """
    Relatório pós-ação (fotos, estatísticas) enviado por um participante.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="reports", verbose_name=_("Evento"))
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_("Autor"))
    content = models.TextField(_("Conteúdo do Relatório"))
    # Em um app real, você usaria um ImageField e configuraria o upload de arquivos.
    # URLField simplifica para o exemplo da API.
    photo_url = models.URLField(_("URL da Foto"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Relatório de Ação")
        verbose_name_plural = _("Relatórios de Ações")

    def _str_(self):
        return f"Relatório para {self.event.title} por {self.author.username}"